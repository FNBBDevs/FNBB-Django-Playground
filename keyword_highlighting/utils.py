


def _chunck_it_out(file, chunk_size=25):
    data = file.read().decode('UTF-8')
    lines = [line.rstrip() for line in data.split('\n')]
    chunks = []

    for i in range(0, len(lines), chunk_size):
        chunks.append({'group':[(j+1, line) for j, line in zip(range(i, i + chunk_size), lines[i:i + chunk_size])]})

    return chunks


def _query_in_group(query, group):
    for i, line in group:
        if query.lower() in line.lower():
            return True
    return False