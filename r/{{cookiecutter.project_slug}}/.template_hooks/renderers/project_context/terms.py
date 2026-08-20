"""Render EDAM-like terms used in public interoperability sections."""


def format_edam_term_label(term_record):
    """Format one EDAM-like term record.

    Parameters
    ----------
    term_record : dict
        Term record with optional ``term`` and ``uri`` keys.

    Returns
    -------
    str
        Human-readable term label.
    """
    term = term_record.get("term", "")
    uri = term_record.get("uri", "")

    if term and uri:
        return f"[{term}]({uri})"
    return term or uri


def format_function_io_label(io_record):
    """Format one function input or output record.

    Parameters
    ----------
    io_record : dict
        Function input or output record.

    Returns
    -------
    str
        Human-readable input/output label.
    """
    data_label = format_edam_term_label(io_record.get("data", {}))
    format_labels = [
        label
        for format_record in io_record.get("format", [])
        if (label := format_edam_term_label(format_record))
    ]

    if data_label and format_labels:
        return f"{data_label} ({', '.join(format_labels)})"
    if data_label:
        return data_label
    return ", ".join(format_labels)
