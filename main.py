// ... existing imports ...
import modal
from fastapi.middleware.cors import CORSMiddleware

// Add gentrace SDK imports for tracing
from gentrace import init, interaction
// ... rest of imports ...

image = (
    modal.Image.debian_slim()
    .apt_install("git")
    .pip_install("fastapi", "pydantic", "codegen", "uvicorn", "gentrace-py")  // Include gentrace SDK for instrumentation
)

// ... existing code up to modify_document ...
@app.post("/modify-doc")
async def modify_document(request: DocModificationRequest):
    CODEGEN_ORG_ID_STR = os.getenv("CODEGEN_ORG_ID")
    CODEGEN_TOKEN = os.getenv("CODEGEN_TOKEN")

    if not CODEGEN_ORG_ID_STR or not CODEGEN_TOKEN:
        raise ValueError("CODEGEN_ORG_ID and CODEGEN_TOKEN must be set in Modal secrets 'codegen-credentials'.")

    try:
        CODEGEN_ORG_ID = int(CODEGEN_ORG_ID_STR)
    except ValueError:
        raise ValueError("CODEGEN_ORG_ID must be an integer.")

    # Initialize gentrace for OpenTelemetry instrumentation
    GENTRACE_API_KEY = os.getenv("GENTRACE_API_KEY", "STUB_API_KEY")   
    GENTRACE_PIPELINE_ID = os.getenv("GENTRACE_PIPELINE_ID", "STUB_PIPELINE_ID")
    init(api_key=GENTRACE_API_KEY, base_url="https://staging.gentrace.ai/api")

    base_prompt_template = ""

    # Helper to run the Agent call under a traced span
    @interaction(pipeline_id=GENTRACE_PIPELINE_ID)
    def traced_agent_run(prompt_text: str):
        return Agent(org_id=CODEGEN_ORG_ID, token=CODEGEN_TOKEN).run(prompt=prompt_text)

    if request.page_context_type == "gentrace_docs":
        # ... existing code for building base_prompt_template ...
        agent = Agent(org_id=CODEGEN_ORG_ID, token=CODEGEN_TOKEN)
        # Dispatch the prompt through gentrace-instrumented call
        task = traced_agent_run(base_prompt_template)
    return {
        "details": base_prompt_template,
        "doc_name": request.doc_name,
        "message": "CodeGen agent dispatched to modify document.",
        "task_id": task.id
    }

// ... rest of file ...
