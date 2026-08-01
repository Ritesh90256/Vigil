CREATE TABLE traces(
    trace_id UUID PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    agent_goal TEXT NOT NULL,
    final_output TEXT
)

CREATE TABLE spans(
    span_id UUID PRIMARY KEY,
    trace_id UUID REFERENCES traces(trace_id),
    parent_span_id UUID REFERENCES spans(span_id),
    type TEXT NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    status TEXT NOT NULL
)

CREATE TABLE tool_calls(
    tool_call_id UUID PRIMARY KEY,
    span_id UUID REFERENCES spans(span_id),
    tool_name TEXT NOT NULL,
    tool_input JSONB NOT NULL,
    tool_output JSONB,
    error_message TEXT
)

CREATE TABLE labels (
    label_id UUID PRIMARY KEY,
    trace_id UUID REFERENCES traces(trace_id),
    label_source TEXT NOT NULL,
    failure_mode TEXT NOT NULL,
    confidence TEXT NOT NULL,
    reasoning TEXT
);