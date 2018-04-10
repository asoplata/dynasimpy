from brian2 import *
import os

class SimulatorOptions:
    def __init__(self):
        # note there is NO vary by default

        # Solver options
        self.solver = 'rk4'
        self.tspan = [0, 100*ms]
        self.dt = 0.01*ms
        # TODO initialize randomization
        self.random_seed = 1

        # Optimization options
        self.compile_flag = False

        # Saved data/results options
        self.save_results_flag = False
        self.save_data_flag = False
        self.overwrite_flag = False
        self.study_dir = os.getcwd()

        # Cluster computing
        self.cluster_flag = False
        self.memory_limit = '8G'

        # Multicore computing
        self.multicore_flag = False

        # Postprocessing
        self.analysis_functions = {}
        self.analysis_options = {}
        self.plot_functions = {}
        self.plot_options = {}

        # original options from dynasim:
        # solver options (provided as key/value pairs: 'option1',value1,'option2',value2,...):
        #   'solver'      : solver for numerical integration (see dsGetSolveFile)
        #                   {'euler','rk2','rk4', or any built-in matlab solver} (default: 'rk4')
        #   'tspan'       : time limits of simulation [begin,end] (default: [0 100]) [ms]
        #                   note: units must be consistent with dt and model equations
        #   'dt'          : time step used for DynaSim solvers (default: .01) [ms]
        #   'downsample_factor': downsampling applied during simulation (default: 1, no downsampling)
        #                   (only every downsample_factor-time point is stored in memory and/or written to disk)
        #   'ic'          : numeric array of initial conditions, one value per state
        #                   variable (default: all zeros). overrides definition in model structure
        #   'random_seed' : seed for random number generator (default: 'shuffle', set randomly) (usage: rng(options.random_seed))
        #   'compile_flag': whether to compile simulation using coder instead of
        #                   interpreting Matlab {0 or 1} (default: 0)
        #   'sparse_flag' : whether to convert numeric fixed variables to sparse matrices {0 or 1} (default: 0)
        #
        # options for running sets of simulations:
        #   'vary'        : (default: [], vary nothing): cell matrix specifying model
        #                   components to vary across simulations (see NOTE 1 and dsVary2Modifications)
        #
        # options to control saved data:
        #   'matCompatibility_flag': whether to save mat files in compatible mode, vs to prioritize > 2GB VARs {0 or 1} (default: 1)
        #   'save_results_flag': whether to save results of analysis and plotting
        #   'save_data_flag': whether to save simulated data to disk after completion {0 or 1} (default: 0)
        #   'overwrite_flag': whether to overwrite existing data files {0 or 1} (default: 0)
        #   'study_dir'     : relative or absolute path to output directory (default: current directory)
        #   'prefix'        : string to prepend to all output file names (default: 'study')
        #   'disk_flag'     : whether to write to disk during simulation instead of storing in memory {0 or 1} (default: 0)
        #   'precision'     : {'single','double'} precision of simulated data saved to disk (default: 'single')
        #
        # options for cluster computing:
        #   'cluster_flag'  : whether to run simulations on a cluster submitted
        #                   using qsub (see dsCreateBatch) {0 or 1} (default: 0)
        #   'sims_per_job'  : number of simulations to run per batch job (default: 1)
        #   'memory_limit'  : memory to allocate per batch job (default: '8G')
        #   'qsub_mode'     : whether to use SGE -t array for 1 qsub, mode: 'array'; or
        #                       qsub in csh for loop, mode: 'loop'. (default: 'loop').
        #   'one_solve_file_flag': only use 1 file of each time when solving (default: 0)
        #   'optimize_big_vary': Select best options for doing many sims {0 or 1} (default: 0)
        #
        # options for parallel computing: (requires Parallel Computing Toolbox)
        #   'parallel_flag' : whether to use parfor to run simulations {0 or 1} (default: 0)
        #   'num_cores'     : number of cores to specify in the parallel pool
        #   *note: parallel computing has been disabled for debugging...
        #
        # options for post-processing:
        #   'analysis_functions': cell array of analysis function handles
        #   'analysis_options'  : cell array of option cell arrays {'option1',value1,...}
        #   'plot_functions'    : cell array of plot function handles
        #   'plot_options'      : cell array of option cell arrays {'option1',value1,...}
        #
        # other options:
        #   'verbose_flag'  : whether to display informative messages/logs (default: 0)
        #   'modifications' : how to modify DynaSim specification structure component before simulation (see dsApplyModifications)
        #   'experiment'    : function handle of experiment function (see NOTE 2)
        #   'experiment_options' : single cell array of key/value options for experiment function
        #   'optimization'  : function handle of optimization function (see NOTE 2)
        #   'debug_flag'    : set to debug mode
        #   'benchmark_flag': set to benchmark mode. will add tic/toc to sims.

    def validate_options(self, options):
        """TODO: Docstring for validate_options.
        :returns: TODO

        """
        print('in validate_options')
        print('--> options, formerly kwargs-vary, is {}'.format(options))
        # Update SimulatorOptions object from dspy.simulate arguments
        for key, value in options.items():
            # TODO check for malformed option
            setattr(self, key, value)

        # TODO actual validation lol
        return(self)



