import subprocess

def run_test_case(test_case):
    test_input = f"MooshakInstances/{test_case}.in"
    expected_output = f"MooshakInstances/{test_case}.out"

    # Run the program and capture the output
    process = subprocess.Popen(['python3', 'bimaru.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open(test_input, 'r') as input_file:
        output, error = process.communicate(input=input_file.read().encode())

    # Compare the output with the expected output
    with open(expected_output, 'r') as expected_file:
        expected = expected_file.read().strip()
        if output.decode().strip() == expected:
            print(f"{test_case}: Passed")
        else:
            print(f"{test_case}: Failed")

# Test all the cases
test_cases = []
for i in range(1, 16):
    if i < 10:
        test_cases.append(f"T0{i}")
    else:
        test_cases.append(f"T{i}")

for test_case in test_cases:
    run_test_case(test_case)
