from concurrent.futures import ThreadPoolExecutor
from json import dumps
from multiprocessing import cpu_count, Pool, Process, Queue
from prettytable import PrettyTable
from random import randint
from time import time


dataset_size = 10000


def generate_data(n: int) -> list[int]:
    return [randint(1, 1000) for i in range(n)]


def factorial(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def worker(process_id: int, input_queue: Queue, output_queue: Queue):
    while True:
        try:
            num = input_queue.get(timeout=1)
            if num is None:
                break
            result = factorial(num)
            output_queue.put((num, result))
        except Exception as e:
            print(f"Error in process {process_id}: {str(e)}")


def main(result_path: str) -> None:
    results: list[dict] = []

    # синхронное выполнение
    curr_time = time()
    data = [factorial(n) for n in generate_data(dataset_size)]
    sync_time = time() - curr_time
    results.append({"Regular execution": sync_time})

    # реализация через треды
    curr_time = time()
    with ThreadPoolExecutor() as executor:
        executor.map(factorial, generate_data(dataset_size))
        threads_time = time() - curr_time
        results.append({"Thread Pool execution": threads_time})

    # реализация через пул процессов 
    curr_time = time()
    with Pool(cpu_count()) as pool:
        pool.map(factorial, generate_data(dataset_size))
        pool_time = time() - curr_time
        results.append({"Process pool execution": pool_time})

    # реализация через процессы с очередями
    curr_time = time()
    input_queue = Queue()
    output_queue = Queue()

    processes: list[Process] = []
    for i in range(cpu_count()):
        p = Process(target=worker, args=(i, input_queue, output_queue))
        processes.append(p)
        p.start()

    for num in data:
        input_queue.put(num)

    for _ in range(cpu_count()):
        input_queue.put(None)

    for p in processes:
        p.join()
    process_time = time() - curr_time
    results.append({"Process pool execution": process_time})

    # принтим таблицу
    table = PrettyTable()
    table.field_names = ["Execution method", "Time"]
    for result in results:
        table.add_row(*list(result.items()))
    print(table)

    #  сохраняем в файл
    with open(result_path, 'w') as resultfile:
        for result in results:
            resultfile.write(dumps(result) + "\n")


if __name__ == '__main__':
    main('./results1.jsonl')