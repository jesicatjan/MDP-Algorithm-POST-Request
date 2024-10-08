class ChecklistUtility:
    def __init__(self):
        self.steps = [
            "Step 1: Connect the Raspberry Pi to the STM via serial.",
            "Step 2: Initialize Bluetooth connection with the Android device.",
            "Step 3: Send a test message from the Android device to the Raspberry Pi.",
            "Step 4: Relay the message from Raspberry Pi to the STM via serial.",
            "Step 5: Verify response from STM and send acknowledgment to Android."
        ]

    def show_checklist(self):
        print("Project Checklist:")
        for step in self.steps:
            print(step)

    def mark_step_done(self, step_number):
        if 0 < step_number <= len(self.steps):
            print(f"Step {step_number} completed.")
        else:
            print(f"Invalid step number: {step_number}")

# Example usage
if __name__ == "__main__":
    checklist = ChecklistUtility()
    checklist.show_checklist()
    checklist.mark_step_done(3)
