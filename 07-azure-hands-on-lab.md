# Lesson 07: Azure from access to extraction and deployment

Goal: explain the identity, endpoint, data contract and failure at every boundary. Start with your project's approved sandbox. Azure account access, allowed regions, quotas, service features and pricing depend on your organisation and subscription; confirm them before provisioning anything. The instructions below do not create resources automatically.

## 1. Prerequisites and access worksheet

Record: tenant, subscription, resource group, region, Document Intelligence resource name, endpoint, permitted data, cost owner, role-assignment owner and cleanup date. Never put keys in that worksheet. Ask for the actual lab repository, expected Python/package versions and deployment service.

With Azure CLI installed, sign in to the approved tenant and inspect the active subscription:

```powershell
az login
az account show --query "{name:name,id:id,tenantId:tenantId}" -o table
# If needed, choose the approved subscription ID interactively:
$practiceSubscription = Read-Host "Approved subscription ID"
az account set --subscription $practiceSubscription
```

The browser's portal session, Azure CLI developer identity and deployed app identity can differ. Record which one each experiment uses. Being able to view/create a resource does not establish permission to call its service API. Use the service's required data permissions with the correct scope; obtain role assignments from the sandbox owner rather than granting yourself broad subscription permissions.

## 2. Offline baseline before spending time on Azure

```powershell
python -m examples.ai_systems validate
python -m examples.ai_systems profile
python -m unittest discover -s tests -v
```

Inspect `data/documents/` and `data/document_manifest.json`. There are three synthetic native-text invoices: clean, missing identifier and adversarial notes. They are original test fixtures, not copies of customer documents. The invoice project teaches extraction and review mechanics; it is not an identity-verification solution.

`data/extraction_fixtures.json` is a hand-authored normalized application format. Its confidence scores are teaching values, not actual Azure measurements. Expected labels are separate in `data/answers/` and must not be passed to the model.

## 3. First live extraction

Use an approved existing Document Intelligence resource, or follow the official exercise to create one in your practice scope. In Studio, run the invoice model on the clean PDF and compare the result with the source. Check the missing-identifier and adversarial versions next. Do not interpret a plausible extraction as a verified document.

Official practice: [Document Intelligence exercises](https://microsoftlearning.github.io/mslearn-ai-document-intelligence/).

Install only the Python dependencies needed for this step:

```powershell
python -m pip install azure-ai-documentintelligence azure-identity
$env:DOCUMENTINTELLIGENCE_ENDPOINT = Read-Host "Document Intelligence resource endpoint"
# Default: use DefaultAzureCredential with a correctly permissioned developer identity.
python -m examples.ai_systems.azure_extract --file data/documents/invoice-clean.pdf --customer-id C-1001
```

For a sandbox explicitly using service keys, set `DOCUMENTINTELLIGENCE_API_KEY` through the approved secret method. The extractor uses the key only when that environment variable is nonempty; otherwise it uses Entra credentials. The resource/endpoint must support the chosen authentication method. Do not reuse an OpenAI/Gemini key for Document Intelligence.

The extractor calls `prebuilt-invoice`, waits with an SDK poller, saves the raw service response and writes `output/azure-normalized.json`. It takes customer ID from the caller's trusted assignment rather than guessing a customer from the document. It expects one invoice per file; a different count requires splitting or review. A timeout can leave service-side processing in progress; inspect request/operation information before resubmitting.

The normalizer maps `InvoiceId`, `VendorName`, `InvoiceDate` and `InvoiceTotal` into the lab schema. Confidence or currency codes may be absent. Inspect the actual raw result instead of filling missing values with invented defaults.

```powershell
python -m examples.ai_systems validate --file output/azure-normalized.json
```

Repeat extraction with the other two PDFs and distinct `--output` paths. Compare values with the manifest; do not expect live confidence values to match the saved JSON fixtures.

## 4. Evaluate extraction and human review

Create field-level labels from the PDF itself. Measure missing/incorrect fields as well as successful extraction. Run the fixtures at different thresholds:

```powershell
python -m examples.ai_systems validate --threshold 0.8
python -m examples.ai_systems validate --threshold 0.9
```

The demo's default 0.85 is an invented training setting. Establish review thresholds from representative labels, business consequences and applicable learning path risk standards. A high-confidence supplier-name mismatch still needs review; missing confidence requires an explicit decision. Read [Microsoft's confidence guidance](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept/accuracy-confidence?view=doc-intel-4.0.0).

The fixture validator treats free-text notes as data. That does not establish that a language model resists injection. Supply the adversarial note to a real model as clearly delimited document content, keep writes disabled, and inspect its proposed calls. Then verify the application's scoped authorization still blocks an unauthorized call.

## 5. Understand local and hosted identity

| Environment | Identity practice | Verification |
|---|---|---|
| Local laptop | Entra developer sign-in through an appropriate credential chain | Identify the account/tenant used and perform one service call |
| Azure-hosted app | Managed identity where the selected service supports it | Grant the identity only the required service-data permissions and call the service from the host |
| Service-key lab | Key supplied securely through configuration | Know where it is stored, rotated and removed; never log it |

When a managed identity is available, adding Key Vault does not mean every service needs a stored key. Keep Key Vault for remaining secrets and follow the approved configuration. See [Microsoft's Python authentication guidance](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/overview) and the [Document Intelligence Python client](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme?view=azure-python).

## 6. Azure OpenAI is a separate model-hosting exercise

If the learning path uses Azure OpenAI, obtain its v1 base URL and accessible model deployment name. The CLI's `--provider openai` calls the direct OpenAI service; it does not target Azure. This optional SDK example demonstrates an Azure call using Entra authentication:

```powershell
python -m pip install openai azure-identity
$env:AZURE_OPENAI_V1_BASE_URL = Read-Host "Azure OpenAI v1 base URL ending /openai/v1/"
$env:AZURE_OPENAI_DEPLOYMENT = Read-Host "Accessible model deployment name"
python -m examples.ai_systems.azure_openai_chat
```

Inspect `examples/ai_systems/azure_openai_chat.py`: it uses the OpenAI Python client with the Azure base URL, an Entra token provider and your deployment name. Verify Responses support for the actual deployment/API. Other Foundry model deployments and Gemini on Vertex AI require their own endpoint/authentication setup; they are not interchangeable credential substitutions.

Reference: [Microsoft's OpenAI/Azure endpoint comparison](https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/switching-endpoints).

## 7. Deployment rehearsal

A first project can finish with a justified deployment plan; a later exercise can deploy and operate it. Use your project's approved hosting path, or a suitable personal learning subscription. [The Container Apps source-deployment tutorial](https://learn.microsoft.com/en-us/azure/container-apps/quickstart-code-to-cloud) is one optional learning route.

Before deploying this practice app, decide how the approved host will provide authentication/private access, environment configuration, durable state and logs. The sample Streamlit UI is a local single-user teaching interface, and the SQLite file is local persistence. A container's ephemeral disk is not a durable multi-instance review database. Use an approved durable store and appropriate access controls for a hosted adaptation.

Evidence to capture:

- A successful request from the deployed environment using its own identity.
- One wrong-configuration/permission failure, the request ID and the first useful log.
- Measured response latency, model steps, token usage and document-processing volume.
- The restart/retry behavior and ownership of unresolved reviews.
- The resource inventory, estimate, budget alerts and cleanup owner/date.

A cost budget alerts you; it does not automatically stop resources or consumption. Bound application loops and service use, and explicitly clean up practice resources you own. See [Microsoft's budget documentation](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets).

## 8. Check your understanding

Explain: why local access can work while a hosted call fails; why a portal role may not allow inference; why a service poller differs from `async`; why an endpoint and deployment name are different; why a valid extraction is not onboarding approval; and what happens after a timeout and restart.
