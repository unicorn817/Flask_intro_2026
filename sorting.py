def _comes_before(left, right, descending):
    return left > right if descending else left < right


def bubble_sort(values, descending=False):
    result = values.copy()
    comparisons = 0
    swaps = 0

    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for index in range(end):
            comparisons += 1
            if _comes_before(result[index + 1], result[index], descending):
                result[index], result[index + 1] = result[index + 1], result[index]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return result, comparisons, swaps


def selection_sort(values, descending=False):
    result = values.copy()
    comparisons = 0
    swaps = 0

    for start in range(len(result) - 1):
        selected = start
        for index in range(start + 1, len(result)):
            comparisons += 1
            if _comes_before(result[index], result[selected], descending):
                selected = index
        if selected != start:
            result[start], result[selected] = result[selected], result[start]
            swaps += 1

    return result, comparisons, swaps


def insertion_sort(values, descending=False):
    result = values.copy()
    comparisons = 0
    moves = 0

    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0:
            comparisons += 1
            if not _comes_before(current, result[position], descending):
                break
            result[position + 1] = result[position]
            moves += 1
            position -= 1
        result[position + 1] = current
        moves += 1

    return result, comparisons, moves


def merge_sort(values, descending=False):
    comparisons = 0
    moves = 0

    def sort(items):
        nonlocal comparisons, moves
        if len(items) <= 1:
            return items

        middle = len(items) // 2
        left = sort(items[:middle])
        right = sort(items[middle:])
        merged = []
        left_index = 0
        right_index = 0

        while left_index < len(left) and right_index < len(right):
            comparisons += 1
            if _comes_before(right[right_index], left[left_index], descending):
                merged.append(right[right_index])
                right_index += 1
            else:
                merged.append(left[left_index])
                left_index += 1
            moves += 1

        merged.extend(left[left_index:])
        merged.extend(right[right_index:])
        moves += len(left) - left_index + len(right) - right_index
        return merged

    return sort(values.copy()), comparisons, moves


def quick_sort(values, descending=False):
    result = values.copy()
    comparisons = 0
    swaps = 0

    def partition(low, high):
        nonlocal comparisons, swaps
        pivot = result[high]
        boundary = low

        for index in range(low, high):
            comparisons += 1
            if _comes_before(result[index], pivot, descending):
                if boundary != index:
                    result[boundary], result[index] = result[index], result[boundary]
                    swaps += 1
                boundary += 1

        if boundary != high:
            result[boundary], result[high] = result[high], result[boundary]
            swaps += 1
        return boundary

    def sort(low, high):
        if low < high:
            pivot_index = partition(low, high)
            sort(low, pivot_index - 1)
            sort(pivot_index + 1, high)

    sort(0, len(result) - 1)
    return result, comparisons, swaps


SORT_ALGORITHMS = {
    'bubble': {
        'title': 'Bubble Sort',
        'description': 'Compares adjacent values and swaps them until the list is in order.',
        'best': 'Small lists and learning sorting basics',
        'time': 'Best O(n), average/worst O(n²)',
        'space': 'O(1)',
        'stable': 'Yes',
        'sort': bubble_sort,
    },
    'selection': {
        'title': 'Selection Sort',
        'description': 'Finds the smallest remaining value and moves it into the next position.',
        'best': 'Small lists or when minimizing swaps',
        'time': 'O(n²) in best, average, and worst cases',
        'space': 'O(1)',
        'stable': 'No',
        'sort': selection_sort,
    },
    'insertion': {
        'title': 'Insertion Sort',
        'description': 'Builds a sorted section by inserting each value into its correct place.',
        'best': 'Small or mostly sorted lists',
        'time': 'Best O(n), average/worst O(n²)',
        'space': 'O(1)',
        'stable': 'Yes',
        'sort': insertion_sort,
    },
    'merge': {
        'title': 'Merge Sort',
        'description': 'Splits the list, sorts each half, and merges the sorted halves.',
        'best': 'Large lists when stable sorting is useful',
        'time': 'O(n log n) in best, average, and worst cases',
        'space': 'O(n)',
        'stable': 'Yes',
        'sort': merge_sort,
    },
    'quick': {
        'title': 'Quick Sort',
        'description': 'Partitions values around a pivot, then sorts each partition.',
        'best': 'Large lists when average speed and low extra memory matter',
        'time': 'Average O(n log n), worst O(n²)',
        'space': 'Average O(log n), worst O(n)',
        'stable': 'No',
        'sort': quick_sort,
    },
}


def sort_values(values, algorithm, descending=False):
    try:
        sort_function = SORT_ALGORITHMS[algorithm]['sort']
    except KeyError:
        raise ValueError('Choose a valid sorting algorithm.') from None
    return sort_function(values, descending)
