"""Reduz o itineraries.csv (~30 GB) aos voos diretos e às colunas usadas no projeto."""

import argparse
import csv
import os
import time
from collections import deque
from functools import partial
from itertools import islice
from multiprocessing import Pool, cpu_count

from tqdm import tqdm

OUTPUT_COLUMNS = [
    "searchDate",
    "flightDate",
    "startingAirport",
    "destinationAirport",
    "totalFare",
    "segmentsAirlineName",
]


def read_chunks(file, chunk_size):
    while chunk := list(islice(file, chunk_size)):
        yield chunk


def filter_chunk(lines, nonstop_idx, output_idx):
    min_length = max(nonstop_idx, *output_idx) + 1
    rows = csv.reader(line.decode("utf-8", errors="ignore") for line in lines)
    filtered = [
        [row[i] for i in output_idx]
        for row in rows
        if len(row) >= min_length and row[nonstop_idx] == "True" and all(row[i] for i in output_idx)
    ]
    return filtered, sum(map(len, lines))


def filter_itineraries(input_path, output_path, chunk_size=50_000, workers=None):
    workers = workers or max(1, cpu_count() - 2)

    with open(input_path, "rb") as infile, open(output_path, "w", newline="", encoding="utf-8") as outfile:
        header_line = infile.readline()
        header = next(csv.reader([header_line.decode("utf-8")]))
        worker = partial(
            filter_chunk,
            nonstop_idx=header.index("isNonStop"),
            output_idx=[header.index(column) for column in OUTPUT_COLUMNS],
        )

        writer = csv.writer(outfile)
        writer.writerow(OUTPUT_COLUMNS)
        rows_written = 0

        with (
            Pool(workers) as pool,
            tqdm(total=os.path.getsize(input_path), initial=len(header_line), unit="B", unit_scale=True) as progress,
        ):
            # Limita os chunks em memória; Pool.imap leria o ficheiro inteiro de uma vez.
            pending = deque()
            chunks = read_chunks(infile, chunk_size)
            while True:
                while len(pending) < 2 * workers and (chunk := next(chunks, None)):
                    pending.append(pool.apply_async(worker, (chunk,)))
                if not pending:
                    break
                rows, size = pending.popleft().get()
                writer.writerows(rows)
                rows_written += len(rows)
                progress.update(size)

    return rows_written


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="data/itineraries.csv")
    parser.add_argument("output", nargs="?", default="data/voos_filtrados.csv")
    parser.add_argument("--chunk-size", type=int, default=50_000)
    parser.add_argument("--workers", type=int)
    args = parser.parse_args()

    start = time.perf_counter()
    rows = filter_itineraries(args.input, args.output, args.chunk_size, args.workers)
    print(f"{rows:,} linhas escritas em {args.output} ({time.perf_counter() - start:.0f}s)")


if __name__ == "__main__":
    main()
