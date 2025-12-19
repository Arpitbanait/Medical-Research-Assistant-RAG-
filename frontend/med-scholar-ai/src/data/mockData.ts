export interface Source {
  id: string;
  title: string;
  authors: string[];
  journal: string;
  year: number;
  pubmedId: string;
  url: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  confidence?: number;
  sources?: Source[];
  isWarning?: boolean;
}

export interface QueryHistoryItem {
  id: string;
  query: string;
  timestamp: Date;
  preview: string;
}

export const mockSources: Record<string, Source[]> = {
  diabetes: [
    {
      id: '1',
      title: 'Metformin as First-Line Treatment for Type 2 Diabetes: A Systematic Review',
      authors: ['Smith, J.', 'Johnson, A.', 'Williams, B.'],
      journal: 'Diabetes Care',
      year: 2023,
      pubmedId: '345678',
      url: 'https://pubmed.ncbi.nlm.nih.gov/345678',
    },
    {
      id: '2',
      title: 'Lifestyle Interventions in Type 2 Diabetes Management',
      authors: ['Chen, L.', 'Kumar, R.'],
      journal: 'Lancet Diabetes & Endocrinology',
      year: 2023,
      pubmedId: '456789',
      url: 'https://pubmed.ncbi.nlm.nih.gov/456789',
    },
    {
      id: '3',
      title: 'WHO Guidelines on Diabetes Treatment 2023',
      authors: ['World Health Organization'],
      journal: 'WHO Technical Report',
      year: 2023,
      pubmedId: 'WHO-2023',
      url: 'https://www.who.int/publications/diabetes-2023',
    },
  ],
  metformin: [
    {
      id: '4',
      title: 'Comparative Efficacy of Metformin vs Insulin in Type 2 Diabetes',
      authors: ['Anderson, M.', 'Thompson, K.', 'Lee, S.'],
      journal: 'New England Journal of Medicine',
      year: 2022,
      pubmedId: '567890',
      url: 'https://pubmed.ncbi.nlm.nih.gov/567890',
    },
    {
      id: '5',
      title: 'Long-term Outcomes of Metformin Monotherapy',
      authors: ['Garcia, R.', 'Martinez, P.'],
      journal: 'JAMA Internal Medicine',
      year: 2023,
      pubmedId: '678901',
      url: 'https://pubmed.ncbi.nlm.nih.gov/678901',
    },
  ],
  alzheimers: [
    {
      id: '6',
      title: 'Amyloid Beta Biomarkers in Early Alzheimer Detection',
      authors: ['Park, J.', 'Wilson, E.', 'Brown, T.'],
      journal: 'Nature Neuroscience',
      year: 2024,
      pubmedId: '789012',
      url: 'https://pubmed.ncbi.nlm.nih.gov/789012',
    },
    {
      id: '7',
      title: 'Tau Protein as a Diagnostic Marker: A Meta-Analysis',
      authors: ['Roberts, A.', 'Davis, C.'],
      journal: 'Alzheimer\'s & Dementia',
      year: 2023,
      pubmedId: '890123',
      url: 'https://pubmed.ncbi.nlm.nih.gov/890123',
    },
  ],
};

export const mockResponses: Record<string, { content: string; confidence: number; sources: Source[] }> = {
  'diabetes': {
    content: `Based on current research evidence, the primary treatments for Type 2 Diabetes include:

**First-Line Treatment:**
- **Lifestyle modifications** including diet and exercise remain the cornerstone of management [1]
- **Metformin** is recommended as first-line pharmacotherapy due to its efficacy, safety profile, and cardiovascular benefits [1][2]

**Second-Line Options:**
When glycemic targets are not achieved with metformin alone:
- SGLT2 inhibitors (empagliflozin, dapagliflozin)
- GLP-1 receptor agonists (semaglutide, liraglutide)
- DPP-4 inhibitors

**Advanced Therapy:**
- **Insulin therapy** is recommended when glycemic control remains inadequate despite oral medications [3]

The WHO 2023 guidelines emphasize individualized treatment based on patient factors including cardiovascular risk, kidney function, and hypoglycemia risk [3].`,
    confidence: 0.86,
    sources: mockSources.diabetes,
  },
  'metformin': {
    content: `**Metformin vs Insulin Efficacy Comparison:**

**Glycemic Control:**
- Both effectively reduce HbA1c levels
- Insulin provides more rapid glucose reduction
- Metformin achieves ~1.0-1.5% HbA1c reduction [1]

**Weight Effects:**
- **Metformin**: Weight neutral or slight loss (-1 to -2 kg)
- **Insulin**: Often associated with weight gain (+2 to +4 kg) [1]

**Cardiovascular Outcomes:**
- Metformin shows cardiovascular protective effects in long-term studies [2]
- Insulin is neutral for cardiovascular outcomes

**Hypoglycemia Risk:**
- **Metformin**: Very low risk
- **Insulin**: Higher risk, requires careful monitoring [1]

**Recommendation:**
Metformin remains first-line due to better tolerability, weight profile, and cardiovascular benefits. Insulin is reserved for advanced disease or when oral agents fail [2].`,
    confidence: 0.91,
    sources: mockSources.metformin,
  },
  'alzheimers': {
    content: `**Current Research on Alzheimer's Biomarkers:**

**Established Biomarkers:**

1. **Amyloid Beta (Aβ42/Aβ40 ratio)**
   - Measurable in CSF and blood plasma
   - Decreased ratio indicates amyloid pathology
   - Blood-based tests now achieving ~90% accuracy [1]

2. **Tau Proteins**
   - Phosphorylated tau (p-tau181, p-tau217, p-tau231)
   - Elevated levels correlate with disease progression
   - P-tau217 shows highest specificity for AD [2]

3. **Neurofilament Light Chain (NfL)**
   - Marker of neurodegeneration
   - Elevated in blood and CSF

**Emerging Biomarkers (2023-2024):**
- GFAP (glial fibrillary acidic protein)
- Synaptic markers (neurogranin)

**Clinical Utility:**
These biomarkers enable earlier diagnosis, potentially 10-15 years before symptom onset, allowing for earlier intervention [1][2].`,
    confidence: 0.82,
    sources: mockSources.alzheimers,
  },
};

export const initialQueryHistory: QueryHistoryItem[] = [
  {
    id: '1',
    query: 'What are current treatments for Type 2 Diabetes?',
    timestamp: new Date(Date.now() - 86400000),
    preview: 'First-line treatment includes lifestyle modifications and Metformin...',
  },
  {
    id: '2',
    query: 'Compare Metformin vs Insulin efficacy',
    timestamp: new Date(Date.now() - 172800000),
    preview: 'Both effectively reduce HbA1c levels, but differ in weight effects...',
  },
];

export const unsafeKeywords = ['dose for me', 'emergency', 'diagnose me', 'my symptoms', 'should i take', 'prescription'];

export const insufficientEvidenceResponse: ChatMessage = {
  id: 'insufficient',
  role: 'assistant',
  content: `**Insufficient Research Evidence**

I was unable to find sufficient high-quality research evidence to answer your question reliably.

This may be because:
- The topic lacks peer-reviewed studies
- Available research is inconclusive
- The question requires clinical judgment beyond current evidence

**Recommendation:** Please consult a healthcare professional or search specialized medical databases like PubMed directly.`,
  timestamp: new Date(),
  confidence: 0,
  sources: [],
};