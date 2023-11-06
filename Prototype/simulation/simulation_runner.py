from pulser import Sequence
from pasqal_cloud import SDK
import dotenv
import os
from pasqal_cloud.device import EmulatorType, EmuTNConfig
from pulser_simulation import QutipEmulator
import datetime
import yaml

class SimulationRunner:

    def __init__(self,
                 configs: str = "runner_default"):
        dotenv.load_dotenv()
        project_id = os.environ.get('PASQAL_PROJECT_ID')
        username = os.environ.get('PASQAL_USERNAME')
        password = os.environ.get('PASQAL_PASSWORD')
        self.sdk = SDK(username=username, password=password, project_id=project_id)

        self.configs = yaml.safe_load(open(
            os.path.join(
                os.path.dirname(__file__),
                "configs",
                f"{configs}.yml"
        )))
        self.max_bond_dim = self.configs["max_bond_dim"]

    def send_batch(self, 
                 seq: Sequence, 
                 runs: int = 50,
                 emulator: EmulatorType = EmulatorType.EMU_TN):
        serialized_sequence = seq.to_abstract_repr()
        job = {"runs": runs, "variables": {}}
        
        # configuration = EmuTNConfig(dt = 10.0, precision ="normal", max_bond_dim = self.max_bond_dim)
        self.batch = self.sdk.create_batch(serialized_sequence, [job], 
                                      emulator=emulator)#, configuration=configuration) 

    def get_last_ordered_job(self):
        return self.sdk.get_batch(self.batch.id).ordered_jobs[0]
    
    def wait_and_get_last_sent_batch(self, wait_time: int = 600):
        start = datetime.datetime.now()
        print("Waiting for the job to complete...")
        while True:
            batch = self.get_last_ordered_job()
            if batch.status not in ["RUNNING", "PENDING"]:
                print(f"Job is done! Status = {batch.status}")
                break
            if (datetime.datetime.now() - start).seconds > 600:
                print("Job taking longer than expected!")
                break
        return batch
    
    def get_batch_by_id(self, id):
        return self.sdk.get_batch(id).ordered_jobs[0]
    
    def simulate_locally(self,
                         seq: Sequence,
                         runs: int = 50):
        simul = QutipEmulator.from_sequence(seq)
        results = simul.run(progress_bar=True)
        counts_dict = results.sample_final_state(N_samples=runs)
        return dict(sorted(counts_dict.items(), key = lambda k : -k[1]))

    