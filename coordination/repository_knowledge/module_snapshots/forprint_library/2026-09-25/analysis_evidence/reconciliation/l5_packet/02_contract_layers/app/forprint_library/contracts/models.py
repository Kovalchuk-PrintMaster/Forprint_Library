"""Моделі контрактів forprint_library.

Контракт описує форму взаємодії між модулями, а ContractVersion описує
конкретну версію цього контракту.
"""

from datetime import date
from typing import Any

from forprint_library.core.enums import ChangeLevel, ContractStatus
from pydantic import BaseModel, Field


class Contract(BaseModel):
    """Логічний контракт без прив'язки до конкретної версії."""

    code: str = Field(..., examples=["prepress.job_request"])
    name: str
    domain: str = Field(..., examples=["prepress"])
    description: str = ""
    owner_module: str | None = None


class ContractVersion(BaseModel):
    """Окрема версія контракту."""

    contract_code: str
    version: str = Field(..., examples=["1.0.0"])
    status: ContractStatus = ContractStatus.DRAFT

    # Дати життєвого циклу.
    effective_from: date | None = None
    deprecated_from: date | None = None
    blocked_from: date | None = None

    # Машинна JSON Schema.
    json_schema: dict[str, Any]

    # Людинозрозуміла документація.
    human_description: str = ""
    human_changelog: str = ""

    # Машинний опис змін, який потім читатиме sync_manager.
    machine_changelog: dict[str, Any] = Field(default_factory=dict)
    change_level: ChangeLevel = ChangeLevel.COSMETIC

    # Політики міграції.
    auto_migration_allowed: bool = False
    migration_strategy: str | None = None
    migration_rules: list[dict[str, Any]] = Field(default_factory=list)

    # Історична сумісність.
    archive_read_allowed: bool = True

    def allows_new_input(self) -> bool:
        """Чи можна приймати нові документи по цій версії."""

        return self.status not in {
            ContractStatus.BLOCKED_FOR_INPUT,
            ContractStatus.READ_ONLY,
            ContractStatus.ARCHIVED,
        }

    def allows_archive_read(self) -> bool:
        """Чи можна читати архівні документи по цій версії."""

        return self.archive_read_allowed
