import streamlit as st
import time
import matplotlib.pyplot as plt
import random

# Title
st.title("🔍 Binary Search Visualizer")

# 🌙 Dark Mode
dark_mode = st.toggle("🌙 Enable Dark Mode")
if dark_mode:
    st.markdown("<style>body { background-color: black; color: white; }</style>", unsafe_allow_html=True)

# 🎲 Random List Generator
if st.button("🎲 Generate Random Sorted List"):
    arr = sorted(random.sample(range(1, 100), 10))
else:
    arr_input = st.text_input("Enter a sorted list (comma separated):", "5, 10, 15, 20, 25, 30, 35, 40")
    arr = list(map(int, arr_input.split(',')))

# 🎯 Target Number Input
target_input = st.text_input("Enter number to search:", "15")
target = int(target_input)

# AI Chat Messages
def ai_guide(step, mid_value, status):
    messages = {
        "start": "Let's start the Binary Search! 🎯",
        "check": f"Checking the middle element: {mid_value}",
        "move_left": "Your number is smaller, searching left ⬅️",
        "move_right": "Your number is larger, searching right ➡️",
        "found": f"Great! Your number {mid_value} is found! 🎉",
        "not_found": "Oops! Number not in the list. 😢"
    }
    st.chat_message("assistant").write(messages[status])

# Binary Search Function with Visualization
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    steps = []

    while left <= right:
        mid = (left + right) // 2
        steps.append((arr[left:right+1], arr[mid], mid))

        ai_guide(len(steps), arr[mid], "check")

        if arr[mid] == target:
            ai_guide(len(steps), arr[mid], "found")
            return mid, steps
        elif arr[mid] < target:
            left = mid + 1
            ai_guide(len(steps), arr[mid], "move_right")
        else:
            right = mid - 1
            ai_guide(len(steps), arr[mid], "move_left")

    ai_guide(len(steps), -1, "not_found")
    return -1, steps

# 🎨 Matplotlib Graph Visualization
def plot_search(arr, left, right, mid):
    colors = ['blue'] * len(arr)
    if left <= right:
        colors[mid] = 'red'

    fig, ax = plt.subplots()
    ax.bar(range(len(arr)), arr, color=colors)
    ax.set_xticks(range(len(arr)))
    ax.set_xticklabels(arr)
    st.pyplot(fig)

# Start Search Button
if st.button("🔍 Start Search"):
    if arr != sorted(arr):
        st.error("List must be sorted for Binary Search!")
    else:
        index, steps = binary_search(arr, target)
        for i, (sublist, mid_value, mid_index) in enumerate(steps):
            st.write(f"**Step {i+1}:** Checking `{mid_value}` in `{sublist}`")
            plot_search(arr, 0, len(arr) - 1, mid_index)
            time.sleep(1)

        if index != -1:
            st.success(f"🎉 Found at index {index}!")
        else:
            st.error(f"❌ Number {target} not found.")

# ⏳ Binary Search Time Estimator
st.sidebar.header("⏳ Search Time Estimator")
n = st.sidebar.number_input("Enter list size:", min_value=10, max_value=1000000, step=10)

def estimate_binary_search_time(n):
    start_time = time.time()
    left, right = 0, n - 1
    while left <= right:
        mid = (left + right) // 2
        right = mid - 1
    end_time = time.time()
    return round((end_time - start_time) * 1000, 5)

if st.sidebar.button("Estimate Time"):
    time_taken = estimate_binary_search_time(n)
    st.sidebar.success(f"Estimated Time: {time_taken} ms ⏳")

# 🎮 Play Binary Search Game
st.sidebar.header("🎮 Binary Search Game")
hidden_number = random.choice(arr)
guess = st.sidebar.number_input("Guess a number:", min_value=min(arr), max_value=max(arr))

if st.sidebar.button("Check Guess"):
    if guess == hidden_number:
        st.sidebar.success(f"🎉 Correct! Found in {len(arr)} steps!")
    elif guess < hidden_number:
        st.sidebar.warning("Go Higher! ⬆️")
    else:
        st.sidebar.warning("Go Lower! ⬇️")
