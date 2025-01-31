import csv
from datetime import datetime
from multiprocessing import Pool, cpu_count
import os
from tqdm import tqdm

def process_chunk(args):
    chunk_data, columns_idx = args
    filtered_rows = []
    
    for row in chunk_data:
        try:
            if len(row) < max(columns_idx.values()):
                continue
                
            if (row[columns_idx['isNonStop']] == 'True' and 
                row[columns_idx['searchDate']] and 
                row[columns_idx['flightDate']] and 
                row[columns_idx['startingAirport']] and 
                row[columns_idx['destinationAirport']] and 
                row[columns_idx['totalFare']] and 
                row[columns_idx['segmentsAirlineName']]):
                
                filtered_row = [
                    row[columns_idx['searchDate']],
                    row[columns_idx['flightDate']],
                    row[columns_idx['startingAirport']],
                    row[columns_idx['destinationAirport']],
                    row[columns_idx['totalFare']],
                    row[columns_idx['segmentsAirlineName']]
                ]
                filtered_rows.append(filtered_row)
        except Exception as e:
            print(f"Erro ao processar linha: {e}")
            continue
            
    return filtered_rows

def process_csv_parallel(input_file, output_file, chunk_size=50000):
    columns_idx = {
        'searchDate': 1,
        'flightDate': 2,
        'startingAirport': 3,
        'destinationAirport': 4,
        'isNonStop': 10,
        'totalFare': 11,
        'segmentsAirlineName': 20
    }
    
    num_processes = max(1, cpu_count() - 2)  
    print(f"Utilizando {num_processes} processos")

    print("Contando total de linhas...")
    total_lines = 0
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        total_lines = sum(1 for _ in f) - 1
    print(f"Total de linhas a processar: {total_lines:,}")

    rows_written = 0
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        writer = csv.writer(outfile)
        writer.writerow(['searchDate', 'flightDate', 'startingAirport', 
                        'destinationAirport', 'totalFare', 'segmentsAirlineName'])
        
        reader = csv.reader(infile)
        next(reader)  
        
        pbar = tqdm(total=total_lines, desc="Processando linhas")
        
        current_chunk = []
        chunks_to_process = []
        
        for i, row in enumerate(reader):
            if not row: 
                continue
                
            current_chunk.append(row)
            
            if len(current_chunk) >= chunk_size:
                chunks_to_process.append((current_chunk, columns_idx))
                current_chunk = []
                
                if len(chunks_to_process) >= num_processes:
                    with Pool(num_processes) as pool:
                        results = pool.map(process_chunk, chunks_to_process)
                        
                        for chunk_results in results:
                            if chunk_results:  
                                writer.writerows(chunk_results)
                                rows_written += len(chunk_results)
                    
                    pbar.update(chunk_size * len(chunks_to_process))
                    chunks_to_process = []
                    
                    
                    print(f"Linhas processadas até agora: {i+1:,}, Linhas escritas: {rows_written:,}")
        
        
        if current_chunk:
            chunks_to_process.append((current_chunk, columns_idx))
            
        if chunks_to_process:
            with Pool(num_processes) as pool:
                results = pool.map(process_chunk, chunks_to_process)
                for chunk_results in results:
                    if chunk_results:
                        writer.writerows(chunk_results)
                        rows_written += len(chunk_results)
        
        pbar.close()
        
    print(f"Total de linhas escritas no arquivo final: {rows_written:,}")

if __name__ == '__main__':
    input_file = 'itineraries.csv'
    output_file = 'voos_filtrados.csv'
    
    print("Iniciando processamento...")
    start_time = datetime.now()
    
    process_csv_parallel(input_file, output_file)
    
    end_time = datetime.now()
    print(f"\nTempo total de processamento: {end_time - start_time}")