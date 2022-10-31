# I4.0 Laboratory Simulation

Simulation and generation of synthetic reliability-related data.

## Production Line Layout and Production Sequence

![production line](images/production_line.png)

1. Warehouse 1 prepares parts for one drone
2. Mobile robot transports parts to assembly track
3. Track transports parts to Cell 1
4. Cell 1 executes assembly step
5. Track transports parts to Cell 2
6. Cell 2 executes assembly step
7. Track transports assembled product to pickup point
8. Mobile robot transports product to Warehouse 2

# Setup

1. Clone repository: `git clone https://github.com/jo-chr/i40lab-simulation.git`
2. Install requirements: `pip install -r requirements.txt`
3. Run `python3 main.py`

# Custom Configuration

Use `config.ini` to configure the simulation.

# Usage & Attribution

If you are using the tool for a scientific project please consider citing our [publication](https://ieeexplore.ieee.org/document/9715410):

    # Plain
    J. Friederich, S. C. Jepsen, S. Lazarova-Molnar and T. Worm, 
    "Requirements for Data-Driven Reliability Modeling and Simulation of Smart Manufacturing Systems,"
    2021 Winter Simulation Conference (WSC), 2021, pp. 1-12, doi: 10.1109/WSC52266.2021.9715410.
   
    # BibTeX
    @inproceedings{friederich_requirements_2021,
        author={Friederich, Jonas and Jepsen, Sune Chung and Lazarova-Molnar, Sanja and Worm, Torben}, 
        booktitle={2021 Winter Simulation Conference (WSC)},
        title={Requirements for Data-Driven Reliability Modeling and Simulation of Smart Manufacturing Systems},
        year={2021},  
        pages={1-12},
        doi={10.1109/WSC52266.2021.9715410}
    }



