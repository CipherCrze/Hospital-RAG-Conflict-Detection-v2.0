"""
Configuration constants for the Hospital RAG Conflict Detection System.
"""
import os

# --- Project Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SAMPLE_DOCS_DIR = os.path.join(PROJECT_ROOT, "sample_documents")
CHROMA_PERSIST_DIR = os.path.join(PROJECT_ROOT, "data", "chroma_db")

# --- Text Chunking ---
CHUNK_SIZE = 800            # Characters per chunk
CHUNK_OVERLAP = 200         # Overlap between consecutive chunks

# --- Embedding Model ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Vector Store ---
COLLECTION_NAME = "hospital_docs"

# --- Retrieval ---
TOP_K = 8                   # Number of chunks to retrieve per query
RELEVANCE_THRESHOLD = 0.25  # Minimum similarity score to keep a chunk

# --- LLM ---
LLM_MODEL = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.2      # Low temperature for factual, grounded answers

# --- Conflict Detection ---
NLI_MODEL = "cross-encoder/nli-deberta-v3-small"
CONTRADICTION_THRESHOLD = 0.65  # NLI contradiction probability threshold (Section 3.1.3)
MAX_PAIRWISE_COMPARISONS = 28   # C(8,2) = 28 for top-8 chunks

# --- Supported File Types ---
SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".txt"]

# --- Prompt Templates ---
RAG_CONFLICT_PROMPT = """You are an expert hospital performance analyst. Answer the user's question based ONLY on the provided document context.

## Critical Instructions
1. Base your answer ONLY on the provided context. Do NOT use external knowledge.
2. If documents contain CONFLICTING information, you MUST explicitly identify and explain the conflicts.
3. Always cite sources using the format [Document Name].
4. Provide a confidence level: High, Medium, or Low.
5. If conflicts exist, explain possible reasons for the discrepancy (different departments, different metrics, different time periods, etc.).
6. Structure your response clearly.

## Document Context
{context}

## Detected Conflicts (from automated analysis)
{conflicts}

## User Question
{question}

{profile_instructions}

## Your Response
Provide:
1. **Answer**: A comprehensive answer acknowledging any conflicting evidence
2. **Conflicting Evidence**: List specific contradictions found (if any)
3. **Resolution Tips**: Profile-specific actionable recommendations
4. **Confidence Level**: High / Medium / Low
5. **Reasoning**: Why you assigned this confidence level, considering any conflicts
"""

# Profile-specific instructions injected into the prompt
PROFILE_INSTRUCTIONS = {
    "ED": """## Profile: Emergency Department (ED)
You are responding to an Emergency Department clinician. They need:
- CONCISE, action-oriented answers (time-critical decisions)
- Focus on patient safety, triage protocols, and acute care metrics
- Highlight any conflicts that affect immediate clinical decisions
- Resolution tips should prioritize: which protocol to follow RIGHT NOW
- Flag anything that could delay patient care or create liability
- Keep technical jargon appropriate for ER physicians/nurses
- Detail Level: BRIEF but precise — bullet points preferred""",

    "FN": """## Profile: Finance Department (FN)
You are responding to a Finance/Accounting staff member. They need:
- DETAILED numerical analysis with exact figures and variances
- Focus on budget impacts, cost drivers, revenue metrics, and financial compliance
- Highlight any conflicts between financial reports and operational data
- Resolution tips should prioritize: which numbers to use for official reporting
- Compare period-over-period trends and flag anomalies
- Include implications for budget forecasting and audit readiness
- Detail Level: COMPREHENSIVE with tables/breakdowns where possible""",

    "AD": """## Profile: Administration (AD)
You are responding to a Hospital Administrator. They need:
- EXECUTIVE SUMMARY style answers with strategic implications
- Focus on cross-departmental patterns, policy compliance, and governance
- Highlight any conflicts that indicate systemic issues or policy gaps
- Resolution tips should prioritize: which department head to consult, what policy to update
- Connect findings to hospital-wide KPIs and accreditation requirements
- Suggest escalation paths and committee review where appropriate
- Detail Level: MODERATE — high-level with supporting evidence""",

    "QX": """## Profile: Quality Assurance (QX)
You are responding to a Quality/Compliance officer. They need:
- THOROUGH evidence-based analysis with full source traceability
- Focus on quality metrics, patient outcomes, compliance gaps, and benchmarks
- Highlight ALL conflicts — even minor discrepancies are significant for QA
- Resolution tips should prioritize: root cause analysis steps and corrective actions
- Reference relevant standards (Joint Commission, CMS, etc.) where applicable
- Recommend specific audit procedures or follow-up investigations
- Detail Level: EXHAUSTIVE — leave no discrepancy unaddressed""",

    "IC": """## Profile: Infection Control (IC)
You are responding to an Infection Control specialist. They need:
- CLINICAL analysis focused on infection rates, HAIs, and prevention protocols
- Focus on infection trends, outbreak indicators, sterilization compliance, and PPE adherence
- Highlight any conflicts between infection data and departmental reports
- Resolution tips should prioritize: immediate containment actions and surveillance changes
- Flag any data suggesting unreported infections or protocol violations
- Recommend epidemiological follow-up where patterns emerge
- Detail Level: DETAILED with clinical specificity""",

    "SG": """## Profile: Surgical Department (SG)
You are responding to a Surgical team member. They need:
- CLINICAL analysis focused on surgical outcomes, complications, and OR metrics
- Focus on complication rates, surgical success metrics, mortality data, and case volumes
- Highlight any conflicts between surgical outcome reports and patient feedback
- Resolution tips should prioritize: which outcome data is most reliable for M&M review
- Compare reported outcomes against expected benchmarks
- Recommend specific case reviews or protocol adjustments
- Detail Level: DETAILED with clinical precision""",
}

def get_profile_instructions(profile_code: str) -> str:
    """Get profile-specific instructions for the prompt."""
    return PROFILE_INSTRUCTIONS.get(profile_code, PROFILE_INSTRUCTIONS["AD"])

CONFLICT_EXPLANATION_PROMPT = """You are analyzing two document excerpts from a hospital's records that appear to contain CONFLICTING information.

Document A ({source_a}):
"{text_a}"

Document B ({source_b}):
"{text_b}"

Briefly explain:
1. What specific claims conflict between these two documents?
2. What might explain this discrepancy (different departments, metrics, perspectives)?
Keep your explanation to 2-3 sentences.
"""
