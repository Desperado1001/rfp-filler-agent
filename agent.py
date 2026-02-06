from pydantic_ai import Agent, RunContext
from typing import List, Optional
import uuid
from models import CellInfo, FillResult, TaskStatus
from excel_handler import ExcelHandler
from rag_service import RAGService
from llm_service import LLMService


class RFPFillerAgent:
    """RFP/问卷填写Agent"""

    def __init__(self):
        self.excel_handler: Optional[ExcelHandler] = None
        self.rag_service = RAGService()
        self.llm_service = LLMService()
        self.results: List[CellInfo] = []

    def process_file(
        self,
        file_path: str,
        output_path: Optional[str] = None
    ) -> FillResult:
        """
        处理Excel文件，自动填写问题
        """
        task_id = str(uuid.uuid4())

        try:
            # 1. 加载Excel
            self.excel_handler = ExcelHandler(file_path)

            # 2. 扫描所有问题
            print(f"正在扫描问题...")
            questions = self.excel_handler.get_all_questions()
            print(f"找到 {len(questions)} 个问题")

            # 3. 逐个处理问题
            self.results = []
            for idx, cell_info in enumerate(questions, 1):
                print(f"\n处理 {idx}/{len(questions)}: {cell_info.question[:50]}...")

                try:
                    # 从RAG获取上下文
                    context = self.rag_service.get_context_for_query(
                        cell_info.question,
                        limit=3
                    )

                    # 使用LLM生成答案
                    if context:
                        rag_response = self.llm_service.generate_answer(
                            cell_info.question,
                            context
                        )
                        cell_info.answer = rag_response.answer
                        cell_info.confidence = rag_response.confidence

                        # 根据置信度决定是否需要人工审核
                        if rag_response.confidence > 0.7:
                            cell_info.needs_review = False
                    else:
                        # 没有找到相关上下文
                        cell_info.answer = "需要人工审核：知识库中未找到相关信息"
                        cell_info.confidence = 0.1
                        cell_info.needs_review = True

                    # 如果答案不是占位符，填写到Excel
                    if "需要人工审核" not in cell_info.answer:
                        self.excel_handler.fill_answer(cell_info, cell_info.answer)
                        print(f"  ✓ 已填写: {cell_info.answer[:50]}...")
                    else:
                        print(f"  ⚠️ {cell_info.answer}")

                except Exception as e:
                    print(f"  ✗ 处理失败: {e}")
                    cell_info.answer = f"处理失败: {str(e)}"
                    cell_info.needs_review = True

                self.results.append(cell_info)

            # 4. 保存结果
            if not output_path:
                output_path = file_path.replace('.xlsx', '_filled.xlsx')

            self.excel_handler.save(output_path)

            # 统计
            filled_count = sum(1 for r in self.results if r.answer and "需要人工审核" not in r.answer)
            needs_review_count = sum(1 for r in self.results if r.needs_review)

            return FillResult(
                task_id=task_id,
                status=TaskStatus.COMPLETED,
                filled_cells=self.results,
                output_file=output_path
            )

        except Exception as e:
            return FillResult(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error=str(e)
            )

        finally:
            if self.excel_handler:
                self.excel_handler.close()

    def get_summary(self) -> dict:
        """获取处理结果的统计摘要"""
        if not self.results:
            return {}

        filled = sum(1 for r in self.results if r.answer and "需要人工审核" not in r.answer)
        needs_review = sum(1 for r in self.results if r.needs_review)
        avg_confidence = sum(r.confidence for r in self.results) / len(self.results)

        return {
            "total_questions": len(self.results),
            "filled": filled,
            "needs_review": needs_review,
            "avg_confidence": round(avg_confidence, 2)
        }

    def test_knowledge_base(self, question: str) -> dict:
        """测试知识库，看能否找到相关答案"""
        context = self.rag_service.get_context_for_query(question, limit=3)

        if not context:
            return {
                "question": question,
                "found": False,
                "answer": "知识库中未找到相关信息"
            }

        rag_response = self.llm_service.generate_answer(question, context)

        return {
            "question": question,
            "found": True,
            "answer": rag_response.answer,
            "confidence": rag_response.confidence,
            "context": context
        }
