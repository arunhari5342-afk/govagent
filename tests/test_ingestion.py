from scripts.ingest_policies import chunk_text


def test_chunk_text():
    text = "one two three four five six seven eight nine ten"

    chunks = chunk_text(
        text,
        chunk_size=5,
        overlap=1,
    )

    assert len(chunks) > 1
    assert "one two three four five" in chunks[0]
