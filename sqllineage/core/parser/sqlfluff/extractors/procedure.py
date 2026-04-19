from sqlfluff.core.parser import BaseSegment

from sqllineage.core.holders import StatementLineageHolder, SubQueryLineageHolder
from sqllineage.core.models import Table
from sqllineage.core.parser.sqlfluff.extractors.base import BaseExtractor
from sqllineage.utils.entities import AnalyzerContext


class ProcedureExtractor(BaseExtractor):
    """
    Stored Procedure lineage extractor.
    """

    SUPPORTED_STMT_TYPES = ["create_procedure_statement"]

    def extract(
        self,
        statement: BaseSegment,
        context: AnalyzerContext,
    ) -> StatementLineageHolder:
        holder = StatementLineageHolder()

        supported_stmts = BaseExtractor.get_supported_statement_types()

        procedure_name = self._find_procedure_name(statement)
        if procedure_name:
            holder.add_write(procedure_name)

        for segment in statement.recursive_crawl(
            "select_statement",
            "insert_statement",
            "update_statement",
            "delete_statement",
            "merge_statement",
        ):
            if segment.type in supported_stmts:
                holder |= self._delegate_to_extractor(segment, context)

        return holder

    def _find_procedure_name(self, statement: BaseSegment) -> Table | None:
        for segment in statement.get_children("object_reference", "procedure_name"):
            return Table(segment.raw)
        return None

    def _delegate_to_extractor(
        self, segment: BaseSegment, context: AnalyzerContext
    ) -> SubQueryLineageHolder:
        from sqllineage.core.parser.sqlfluff.extractors.base import BaseExtractor

        for extractor_cls in BaseExtractor.__subclasses__():
            extractor = extractor_cls(self.dialect, self.metadata_provider)
            if extractor.can_extract(segment.type):
                return extractor.extract(segment, context)
        return SubQueryLineageHolder()
