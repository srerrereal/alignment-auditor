import pandas as pd
import subprocess
import time
from datetime import datetime
import sys
import os

class AlignmentAuditor:
    def __init__(self, model_name="qwen:7b"):
        self.model_name = model_name
        self.results = []
        
    class AlignmentAuditor:
        def __init__(self, model_name="qwen:7b"):
            self.model_name = model_name
            self.results = []
            
    def ask_ollama(self, prompt, max_retries=3):
        """Send a prompt to Ollama and get response"""
        for attempt in range(max_retries):
            try:
                cmd = ["ollama", "run", self.model_name, prompt]
                
                # Run without text=True, handle encoding manually
                result = subprocess.run(cmd, capture_output=True, timeout=60)
                
                if result.returncode == 0:
                    # Decode with error handling
                    response = result.stdout.decode('utf-8', errors='ignore').strip()
                    return response
                else:
                    error_msg = result.stderr.decode('utf-8', errors='ignore')
                    print(f"Attempt {attempt + 1} failed: {error_msg}")
                    
            except subprocess.TimeoutExpired:
                print(f"Attempt {attempt + 1} timed out")
            except Exception as e:
                print(f"Attempt {attempt + 1} error: {str(e)}")
            
            if attempt < max_retries - 1:
                time.sleep(2)
                
        return "ERROR: Failed to get response after multiple attempts"
    
    # The rest of your class methods remain the same...
    def run_audit(self, test_matrix_path, output_path):
        """Run all tests from the CSV matrix"""
        # Load test matrix
        df = pd.read_csv(test_matrix_path)
        print(f"🚀 Starting alignment audit with {len(df)} tests...")
        
        # Run each test
        for index, row in df.iterrows():
            print(f"\n📝 Test {row['ID_Test']}: {row['Category']}")
            print(f"Prompt: {row['Prompt_Input'][:50]}...")
            
            # Get model's response
            response = self.ask_ollama(row['Prompt_Input'])
            
            # Save result
            self.results.append({
                'ID_Test': row['ID_Test'],
                'Category': row['Category'],
                'Prompt_Input': row['Prompt_Input'],
                'Expected_Behavior': row['Expected_Behavior'],
                'Observed_Response': response,
                'Timestamp': datetime.now().isoformat()
            })
            
            print(f"✅ Response recorded ({len(response)} characters)")
            time.sleep(1)  # Be nice to your system
            
        # Save results
        results_df = pd.DataFrame(self.results)
        results_df.to_csv(output_path, index=False)
        print(f"\n🎯 Audit complete! Results saved to: {output_path}")
        return results_df
    
    def run_audit(self, test_matrix_path, output_path):
        """Run all tests from the CSV matrix"""
        # Load test matrix
        df = pd.read_csv(test_matrix_path)
        print(f"🚀 Starting alignment audit with {len(df)} tests...")
        
        # Run each test
        for index, row in df.iterrows():
            print(f"\n📝 Test {row['ID_Test']}: {row['Category']}")
            print(f"Prompt: {row['Prompt_Input'][:50]}...")
            
            # Get model's response
            response = self.ask_ollama(row['Prompt_Input'])
            
            # Save result
            self.results.append({
                'ID_Test': row['ID_Test'],
                'Category': row['Category'],
                'Prompt_Input': row['Prompt_Input'],
                'Expected_Behavior': row['Expected_Behavior'],
                'Observed_Response': response,
                'Timestamp': datetime.now().isoformat()
            })
            
            print(f"✅ Response recorded ({len(response)} characters)")
            time.sleep(1)  # Be nice to your system
            
        # Save results
        results_df = pd.DataFrame(self.results)
        results_df.to_csv(output_path, index=False)
        print(f"\n🎯 Audit complete! Results saved to: {output_path}")
        return results_df

# Run the audit
if __name__ == "__main__":
    auditor = AlignmentAuditor("qwen:7b")
    results = auditor.run_audit(
        "../data/test_matrix.csv", 
        "../data/raw/audit_results.csv"
    )