# DINoMe
This repository include three submodules: 
1. chipyard with our Tiny configurations for NormalCache, ScatterCache, and PhantomCache, defined in `chipyard/generators/example/src/main/scala/NormalConfig.scala`, `chipyard/generators/example/src/main/scala/ScatterConfig.scala`, `chipyard/generators/example/src/main/scala/PhantomConfig.scala`;
3. yosys with a modified SMT2 transformer to generate transition formula and initial state;
4. cryptominisat_DINoMe: Implementation for postcondition construction, and count/ sample <S, S', C, I> tuples;

and two folders:
1. ML: ML related codes for feature engineer and rule generations; (under xgboost)
  * Train rules using interference sample and noninterference sample; (train_bits.py)
  * Organizing rules by sorting and dropping rules (Fig. 18); (rule.py)
3. process: include bash/python scripts for experiments and software payload for case studies.
  * Prerequisite1: You should build yosys and build your verilog code (e.g., `make verilog CONFIG=NormalTinyBoomConfigS4W4` in chipyard) to a directory with boom.ys (e.g., process/normal/cache-S4W4). 
  * Prerequisite2: to composse multi-cycle postcondition, counting and sampling solutions, you should install compose, count, and sampler binaries using https://github.com/DINoMe-Project/cryptominisat
  * Under process/normal/cache-S4W4, run `yosys boom.ys` converts verilog code to SMT2 transition logic and initialization logic for a tiny BOOM with 4-way 4-set cache. This may takes minutes to an hour. 
  * process/script/cache_observe.sh is one-step script to generate postcondition for cache-based side channel examples, it would generate a directory states with s${cycle}.cnf. This may takes long depending on how many cycles you want. By default, we simplify the CNF per cycle. You can tweak this by updating generate_cnf.sh

