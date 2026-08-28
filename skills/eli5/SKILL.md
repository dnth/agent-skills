---
name: eli5
description: Create a dead-simple visual explanation for a complete beginner. Use only when the user explicitly invokes /eli5 or starts a request with ELI5; do not trigger for ordinary requests to explain or visualize.
---

# ELI5

Explain the requested topic to someone with no background knowledge. Use the topic in the user's request; clients that provide `$ARGUMENTS` may use that value.

Acknowledgment: This independent implementation was prompted by Thariq Shihipar's MIT-licensed [community `eli5` plugin](https://github.com/anthropics/claude-plugins-community/tree/main/eli5).

## Process

### 1. Find the first useful model

For a mechanism, reduce the topic to:

```text
thing → action → result
```

For a concept, show its defining relationship and one consequence or example. Leave secondary details out.

### 2. Preserve technical truth

Write the literal mechanism in plain language before choosing an analogy. Verify current, disputed, safety-critical, or domain-specific claims with trustworthy sources when tools are available.

If an analogy helps, use one and state where it stops matching reality. Simple means compressed, not false.

### 3. Choose the smallest effective visual

| Need | Format |
|---|---|
| One causal chain | Plain-text arrows or a tiny diagram |
| Sequence or exchange | Mermaid sequence diagram |
| Parts inside a system | Labeled box diagram |
| Before-and-after state | Side-by-side comparison |
| Spatial, animated, or interactive idea | Focused HTML artifact |
| User explicitly requests HTML or big pictures | Focused HTML artifact |

Do not generate HTML by default. A small diagram is better than a decorative webpage when both teach the same thing.

### 4. Deliver the explanation

Include:

1. **One-sentence answer** — what it is and why it matters.
2. **Visual model** — the causal or structural relationship.
3. **Concrete example** — one familiar situation.
4. **Technical terms** — only the names the learner can now attach to the model.
5. **Check** — one “what happens next?” prediction.

Use ordinary verbs such as sends, stores, checks, copies, waits, and blocks. Introduce a technical term only after showing the idea it names.

## HTML Artifacts

When HTML is justified, put the same five-part explanation inside one self-contained `.html` file. Use large type, strong contrast, meaningful visuals, mobile-responsive layout, keyboard support, and reduced-motion support.

Avoid external network requests unless the user requests external assets. Do not publish or share the artifact unless asked. Open or deliver the file when the environment supports it.

## Guardrails

- Address the learner as intelligent and unfamiliar with the topic; avoid baby talk.
- Use one analogy consistently rather than switching metaphors.
- Make every label, arrow, image, and animation carry explanatory meaning.
- Preserve conditions or uncertainty that would change the answer.
- Stop after the first useful model instead of teaching the entire field.
- Return the explanation itself, not a preamble about how it was produced.
