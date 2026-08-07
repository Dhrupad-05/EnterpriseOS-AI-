# ADR 003: Approval interrupts

Human approval is a LangGraph interrupt backed by an approval queue. The graph pauses with durable context and resumes only from an explicit decision.
