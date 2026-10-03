from __future__ import annotations

from dataclasses import dataclass

from .models import RoleContract, SkillContract


@dataclass
class Registry:
    roles: dict[str, RoleContract]
    skills: dict[str, SkillContract]

    @property
    def active_roles(self) -> int:
        return 0

    @property
    def loaded_skills(self) -> int:
        return 0


def build_default_registry() -> Registry:
    roles = {
        "media.content-planner": RoleContract(
            id="media.content-planner",
            industry="media",
            name="Content Planner / 内容策划",
            responsibility="将主题、事实和输入材料转化为内容成果。",
            owned_outputs=("title-list", "article", "outline", "script", "image-brief"),
            allowed_skills=(
                "media.research",
                "media.source-verification",
                "media.content-structure",
                "media.title-writing",
                "media.longform-writing",
            ),
            forbidden_scope=("actual-image-generation", "platform-publishing", "account-operation"),
        ),
        "media.creative-producer": RoleContract(
            id="media.creative-producer",
            industry="media",
            name="Creative Producer / 内容制作",
            responsibility="将已确认内容转化为视觉与多媒体成果。",
            owned_outputs=("cover", "article-image", "visual-package"),
            allowed_skills=(
                "media.visual-direction",
                "media.article-image-generation",
                "media.image-content-matching",
            ),
            forbidden_scope=("redefine-core-article-view", "platform-publishing"),
        ),
        "media.growth-operator": RoleContract(
            id="media.growth-operator",
            industry="media",
            name="Growth Operator / 运营增长",
            responsibility="负责平台适配、发布准备和表现复盘。",
            owned_outputs=("platform-package", "publishing-check", "performance-review"),
            allowed_skills=(
                "media.wechat-adaptation",
                "media.publishing-check",
                "media.performance-analysis",
            ),
            forbidden_scope=("rewrite-professional-source-facts", "publish-without-human-gate"),
        ),
        "engineering.commercial": RoleContract(
            id="engineering.commercial",
            industry="engineering",
            name="Commercial / 商务造价",
            responsibility="负责 BOQ、工程量、价格、变更和费用影响。",
            owned_outputs=("boq-diff", "quantity-review", "cost-impact"),
            allowed_skills=(
                "engineering.boq-parse",
                "engineering.boq-feature-diff",
                "engineering.missing-item-detection",
                "engineering.quantity-review",
            ),
        ),
        "engineering.technical": RoleContract(
            id="engineering.technical",
            industry="engineering",
            name="Technical / 技术工程",
            responsibility="负责图纸、技术变化和专业技术判断。",
            owned_outputs=("drawing-diff", "change-object"),
            allowed_skills=("engineering.drawing-version-compare",),
        ),
        "engineering.production": RoleContract(
            id="engineering.production",
            industry="engineering",
            name="Production / 生产管理",
            responsibility="负责计划、现场生产与进度。",
            owned_outputs=("progress-review", "site-event"),
            allowed_skills=("engineering.progress-tracking",),
        ),
        "engineering.qa-records": RoleContract(
            id="engineering.qa-records",
            industry="engineering",
            name="QA / Records / 质量资料",
            responsibility="负责试验、检验、质量与资料完整性。",
            owned_outputs=("test-report-check", "evidence-package"),
            allowed_skills=("engineering.test-report-check",),
        ),
        "engineering.hse": RoleContract(
            id="engineering.hse",
            industry="engineering",
            name="HSE / 安全管理",
            responsibility="负责安全检查、隐患与整改记录。",
            owned_outputs=("hazard-record",),
            allowed_skills=("engineering.hazard-register",),
        ),
    }

    def skill(id: str, owner: str, purpose: str, inputs: tuple[str, ...], outputs: tuple[str, ...]):
        return SkillContract(
            id=id,
            owner_scope=owner,
            purpose=purpose,
            accepted_inputs=inputs,
            produced_outputs=outputs,
            validation=("required-output-present",),
        )

    skills = {
        "media.research": skill("media.research", "media.content-planner", "内容研究", ("topic",), ("research-notes",)),
        "media.source-verification": skill("media.source-verification", "media.content-planner", "来源核验", ("claims",), ("verified-sources",)),
        "media.content-structure": skill("media.content-structure", "media.content-planner", "内容结构", ("topic",), ("outline",)),
        "media.title-writing": skill("media.title-writing", "media.content-planner", "标题生成", ("topic", "article"), ("title-list",)),
        "media.longform-writing": skill("media.longform-writing", "media.content-planner", "长文写作", ("outline", "topic"), ("article",)),
        "media.visual-direction": skill("media.visual-direction", "media.creative-producer", "视觉方向", ("article",), ("visual-direction",)),
        "media.article-image-generation": skill("media.article-image-generation", "media.creative-producer", "文章配图", ("article", "visual-direction"), ("article-image",)),
        "media.image-content-matching": skill("media.image-content-matching", "media.creative-producer", "图文匹配", ("article", "article-image"), ("visual-package",)),
        "media.wechat-adaptation": skill("media.wechat-adaptation", "media.growth-operator", "公众号适配", ("article", "visual-package"), ("platform-package",)),
        "media.publishing-check": skill("media.publishing-check", "media.growth-operator", "发布前检查", ("platform-package",), ("publishing-check",)),
        "media.performance-analysis": skill("media.performance-analysis", "media.growth-operator", "公众号表现分析", ("metrics",), ("performance-review",)),
        "engineering.boq-parse": skill("engineering.boq-parse", "engineering.commercial", "解析 BOQ", ("boq",), ("boq-structure",)),
        "engineering.boq-feature-diff": skill("engineering.boq-feature-diff", "engineering.commercial", "清单特征差异", ("boq-a", "boq-b"), ("boq-diff",)),
        "engineering.missing-item-detection": skill("engineering.missing-item-detection", "engineering.commercial", "漏项识别", ("boq-a", "boq-b"), ("missing-items",)),
        "engineering.quantity-review": skill("engineering.quantity-review", "engineering.commercial", "工程量复核", ("quantity-data",), ("quantity-review",)),
        "engineering.drawing-version-compare": skill("engineering.drawing-version-compare", "engineering.technical", "图纸版本比对", ("drawing-a", "drawing-b"), ("drawing-diff",)),
        "engineering.progress-tracking": skill("engineering.progress-tracking", "engineering.production", "进度跟踪", ("site-data",), ("progress-review",)),
        "engineering.test-report-check": skill("engineering.test-report-check", "engineering.qa-records", "试验报告检查", ("test-report",), ("test-report-check",)),
        "engineering.hazard-register": skill("engineering.hazard-register", "engineering.hse", "安全隐患整理", ("site-observation",), ("hazard-record",)),
    }
    return Registry(roles=roles, skills=skills)
