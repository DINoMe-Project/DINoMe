# DINoMe
This repository include three submodules: 
1. chipyard with our Tiny configurations and modified cache modules;
2. yosys with a modified SMT2 transformer to generate transition formula and initial state;
3. cryptominisat_DINoMe: Implementation for postcondition construction, and count/ sample <S, S', C, I> tuples;

and two folders:
1. ML: ML related codes for feature engineer and rule generations; (under xgboost)
  * Train rules using interference sample and noninterference sample; (train_bits.py)
  * Organizing rules by sorting and dropping rules (Fig. 18); (rule.py)
3. process: include bash/python scripts for experiments and software payload for case studies.
  * Prerequisite1: You should build yosys and build your verilog code (e.g., `make verilog CONFIG=NormalTinyBoomConfigS4W4` in chipyard) to a directory with boom.ys (e.g., process/normal/cache-S4W4). 
  * Prerequisite2: to composse multi-cycle postcondition, counting and sampling solutions, you should install compose, count, and sampler binaries using https://github.com/DINoMe-Project/cryptominisat
  * Under process/normal/cache-S4W4, run `yosys boom.ys` converts verilog code to SMT2 transition logic and initialization logic for a tiny BOOM with 4-way 4-set cache. This may takes minutes to an hour. 
  * process/script/cache_side_channel.sh is one-step script to generate postcondition for cache-based side channel examples, it would generate a directory states with s${cycle}.cnf. This may takes long depending on how many cycles you want.

