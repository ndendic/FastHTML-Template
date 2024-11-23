from typing import Optional
from fasthtml.common import *
from fh_frankenui.core import *


class Pagination:
    def __init__(
        self,
        base_url: str,
        current_page: int,
        total_pages: int,
        per_page: int,
        target: str = "#table-container",
    ):
        self.base_url = base_url
        self.total_pages = max(1, total_pages)
        self.current_page = max(1, min(current_page, self.total_pages))
        self.per_page = max(1, per_page)
        self.target = target

    def _page_link(self, icon: str, page: Optional[int], disabled: bool) -> UkIconLink:
        if page is None:
            page = self.current_page

        page = max(1, min(page, self.total_pages))

        is_disabled = (
            disabled
            or (icon in ["chevrons-left", "chevron-left"] and self.current_page <= 1)
            or (
                icon in ["chevrons-right", "chevron-right"]
                and self.current_page >= self.total_pages
            )
        )
        return UkIconLink(
            icon=icon,
            button=True,
            disabled=is_disabled,
            hx_get=f"{self.base_url}?page={page}&per_page={self.per_page}",
            hx_target=self.target,
            cls="cursor-pointer"
            if not is_disabled
            else "opacity-50 cursor-not-allowed",
        )

    def __ft__(self, total_records: int, total_table_records: int) -> DivFullySpaced:
        # Recalculate pages based on actual records
        actual_total_pages = max(
            1, (total_table_records + self.per_page - 1) // self.per_page
        )
        self.total_pages = actual_total_pages
        self.current_page = max(1, min(self.current_page, actual_total_pages))

        return DivFullySpaced(cls="mt-4 px-2 py-2")(
            Div(
                f"{total_records} out of {total_table_records} record(s) shown.",
                cls="flex-1 text-sm text-muted-foreground",
            ),
            Div(cls="flex flex-none items-center space-x-8")(
                DivCentered(
                    f"Page {self.current_page} of {self.total_pages}",
                    cls="w-[100px] text-sm font-medium",
                ),
                DivLAligned(
                    # Remove False parameter to let _page_link handle disabled state
                    self._page_link("chevrons-left", 1, disabled=False),
                    self._page_link(
                        "chevron-left", self.current_page - 1, disabled=False
                    ),
                    self._page_link(
                        "chevron-right", self.current_page + 1, disabled=False
                    ),
                    self._page_link("chevrons-right", self.total_pages, disabled=False),
                ),
            ),
        )
