curl http://localhost:8000/v1/completions \
-H "Content-Type: application/json" \
-d @- <<EOF
{
  "model": "/app/models/Skywork-o1-Open-Llama-3.1-8B-awq",
  "prompt": "
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You are an expert programmer and algorithm designer. Your goal is to provide a comprehensive and high-quality solution to the user's coding problem.

You MUST follow this three-part structure precisely:

### 1. Planning Phase
First, think through the problem.
- **Restate the Goal:** Briefly summarize the objective.
- **Algorithm Choice:** State the algorithm you will use (e.g., Recursion with Memoization, Dynamic Programming, etc.) and briefly justify why it's a good fit.
- **High-Level Plan:** Outline the key steps your code will take to implement the algorithm. Mention any important data structures you'll need.
- **Edge Cases:** Identify any edge cases to consider (e.g., empty input, single number expression).

### 2. Code Solution
Second, provide the complete, runnable, and well-commented code solution in Python 3. The code should be enclosed in a single markdown block.

### 3. Solution Explanation
Finally, explain your code.
- **Detailed Walkthrough:** Explain the logic of the code, function by function, connecting it back to your high-level plan.
- **Complexity Analysis:** State the Time Complexity and Space Complexity of your solution and briefly explain why.
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
Solve the following programming problem:

**241. Different Ways to Add Parentheses**

Given a string expression of numbers and operators, return all possible results from computing all the different possible ways to group numbers and operators. You may return the answer in any order.

The operators are +, -, and *.

**Example 1:**
- Input: expression = \"2-1-1\"
- Output: [0, 2]
- Explanation:
((2-1)-1) = 0
(2-(1-1)) = 2

**Example 2:**
- Input: expression = \"2*3-4*5\"
- Output: [-34, -14, -10, -10, 10]
- Explanation:
(2*(3-(4*5))) = -34
((2*3)-(4*5)) = -14
((2*(3-4))*5) = -10
(2*((3-4)*5)) = -10
(((2*3)-4)*5) = 10
<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>\n\n",
  "max_tokens": 30000,
  "temperature": 0.0,
  "repetition_penalty": 1.15,
  "stop": ["<|eot_id|>", "<|end_header_id|>", "\n\n\n"],
  "frequency_penalty": 0.2,
  "presence_penalty": 0.1
}
EOF
