def pizza_numbers(num_slices):
    # Create a list of numbers from 1 to num_slices
    nums = list(range(1, num_slices+1))

    # Divide the list into two halves and reverse the second half
    half = len(nums) // 2
    nums = nums[:half] + nums[half:][::-1]

    # Reorder the numbers in a spiral-like pattern
    pizza_nums = []
    while nums:
        pizza_nums.extend(nums.pop(0) for _ in range(half))
        nums.reverse()

    # Add zeros to the list to match the length of the pizza shape
    pizza_nums += [0] * (num_slices - len(pizza_nums))

    # Apply the pattern of values from the table to the pizza shape
    pizza_cell_gap = []
    for i in range(num_slices):
        row = []
        for j in range(5):
            cell = num_slices - i - 1
            if i < half and j == 2:
                # Create a missing slice for the top half of the pizza
                row.append(0)
            elif i >= half and j == 1:
                # Create a missing slice for the bottom half of the pizza
                row.append(0)
            elif j == 0:
                row.append(-1)
            elif j == 1:
                row.append(pizza_nums[cell] * 2 - 1)
            elif j == 2:
                row.append(-pizza_nums[cell] * 2 - 1)
            else:
                row.append(-8)
        pizza_cell_gap.append(row)

    return pizza_cell_gap


def print_pizza(pizza):
    for row in pizza:
        print(" ".join(str(cell).rjust(3) for cell in row))


pizza = pizza_numbers(12)
print_pizza(pizza)
