formalize the following, break into specific individual pieces:
- sw dev TODO:
    - need to figure out "requirements", i.e. what data format works with gimbl-vis and is possibly conducive to any of the standardized formats like sonata
    - at end of sim, call single analysis "script" (read: function) that user assembles, so data can sit in memory and don't need to save to disk before plotting
    - all "non-essential" (aka not just linear combination) of data saved after sim, but only that (no LFP/MUA activity saved by sim, but instead saved by analysis script
    - post-hoc analysis includes PAC, also analysis of MUA/LFP, need to rethink 
    - instead of making setup fully compatible with Sonata, can just model if after Sonata on a first pass and then get it working, then after phd make it work formally with sonata
        - using this as example: https://github.com/AllenInstitute/sonata/tree/master/examples/300_cells

- omfg eval "psyrun" package for param explor and batch distr https://github.com/jgosmann/psyrun
- "perfect is the enemy of the good", there's a difference b/w doing it beautifully and doing it in time to finish phd

- base_model vs parametrized_model
- yaml mech files could form basis of EVENTUAL NeuroML mech integration

- do NOT allocate time to learning as a prerequisite before coding right now, since 1. most important thing is to finish, even if code is ugly, and 2. need to continuously learn anyways, and 3. don't go around rewriting code unless specifically in "refactoring" phase

# s6-python-dynasimpy :dspy:s6:

## assumptions (need to write down as go along)

### user needs to make sure every parameter is unique in any population/neuron
type

## Next Actions :dynasimpy:

### TODO [#X] clean s6 todos

### [#X] if ALWAYS have access to tree structure of specification, do you EVER
need to combine namespaces with underscores? maybe not
- if don't need to mangle namespaces, then do NOT need to have double
  namespacing
- copy dsApplyModifications interface, (<pop/cxn>, <var name>, value)
- key difference is that in DS, we have to use var names to show our
  namespacing and we don't have structure for it
    - if our data is hdf5, then we don't have to worry
    - if exporting to DS data ans (maybe unnecessary), then can rename vars
      post hoc

### [#X] probably easier to just say "use diff synapse objects for diff mechs,
even between same pops", since WAAY easier to prog
- can then, for "synapse of mech this", can just use synapses[index] for all
  stuff
- agg damn maybe not, since want to do multiple mechs in intrinsic mech call,
  and so already have to org it

### [#X] fully abstract structs and funcs of "the dynasim interface" in the
most abstract sense possible
- this will help both understand DS better and also provide framework for
  reimplementation

### [#X] setup bit perfect test b/w DS and B2, then test in DSPY

### need new name, disconnected from dynasim, but cite for inspiration

### if going to play with this, need to build it in steps
- document install/run steps along entire way as building
    - hopefully, some details like dynasim "model specification" can be applied
      after the fact!
        - would need to work out detail of each B2 and DS "model specs"
          definitions, and then compare so as to translate
- translate TCRE synapses into event-driven types
- implement TCRE and run single in brian2
- implement simplest n=2 sims in pypet for 2 TCRE param values
- compartmentalize TCRE equations/mechs in way that works with pypet and brian2
  (hopefully trivial)
- get simple pypet case running with local scoop multiprocessing
- get single batch run with scoop
- get simple n=2 batch run with scoop, using pypet
- to make dynasim-compatible, should maybe then tie everything together into
  SINGLE INTERFACE

### Batch distributed runs may not work with sumatra
- <https://groups.google.com/forum/m/#!topic/sumatra-users/pkIoNn2VuPI>
- Read sumatra forums about batch queue

### [#Z] data format?
- probably not either the new NWB and or the new Brainformat, because:
    - do not make any claims to support simulation at all
    - more complex than we need
- review Zugaro presentation PDF in s6 folder
- NSDF?

### [#Z] try Parameters package for parametrization

### [#Z] ask brian people about why, in the examples (and working code), dv/dt
is in units of volt only, while this intro page
<http://brian2.readthedocs.io/en/stable/resources/tutorials/1-intro-to-brian-neurons.html?highlight=hertz>
implies that "dv/dt" should REALLY be, in the brian unit system, in units of
"volt / second". Specifically, trying "volt / second" for dv/dt gives a
Dimension error that neuron.v needs to be in volt / second, not volt! so it
seems B2 is using the SAME units for v and dv/dt
- basically, brian2 seems to use the same units for v AND dv/dt, despite the
  tutorial saying one thing and the examples another!
- units thingy relevant to
  <http://brian2.readthedocs.io/en/2.0rc/user/equations.html>
- update: apparently the SV vs dSV/dt distinction is not unique to voltage, as
  it also applies to mNa (when dmNa/dt is given units of Hz)

### [#Z] in Brian2, how to obtain the exact, realized value for the # of source
cells going to a target cell?
- google N_pre in brian forums and issues, since the summed "total" seems to be
  N_actualpre*sSYN

### [#Z] try getting pypet to save diff points in trajectory to diff data files

### [#Z] write dspy spec converter based on regex spaghetti

### [#Z] study <http://pypet.readthedocs.io/en/latest/manual/tutorial.html>

### [#Z] maybe separate DS "interface" (i.e. the trivial one) for programming
brian specifically
- what functionality exactly do we need to replicate DS-style interface on top
  of Brian?
      - specification xfer
      - analysis (hard, only going to get harder)
      - finding and integrating predefined model files
      - variation
      - batch distribution
      - potential problems:
          - DS "model structure" like in dsCheckModel prob not compatible with
            B2 NGroups and SGroups. But that's probably the point - JS is
            treating the "DS spec" of a model as indep from the DS
            implementation of the model as it actually runs it, so likely the
            whole POINT of the "spec" is to be sim-independent
              - e.g. things like "solve files" don't matter for the UI
                (although impo for other reasons like provenance)
              - this thinking is basically like "the spec (and sim options) is
                the only thing the user needs to know"
              - another thing: the DS repr of the MODEL (incl namespaces, etc.)
                doesn't need to be same as B2, since that's implementation
                  - this is where we can leverage B2
          - from fig 9, ONLY expected UI of DS is 1. spec and 2. sim options.
            So EVERYTHING after that point is to be taken care of by the prog,
            not the user, so implementation farther in process doesn't need to
            be identical
              - embedded in this simple UI is ans, variation, batch
                distribution, predef mechs
      - ways to improve:
          - better diffxn for analysis
      - what does the final product look like?
          - DS-style spec of the model (incl pre-def mechs or eqns), and sim
            options incl variations
          - same-style runscripts in python, where only call is dsSimulate?
      - note: DS appears to ALWAYS form a solve file? good idea
      - how to begin progging: start writing the most basic pydsSimulate (from
        fig 9):
        - dsCheckSpecification (same)
        - dsGenerateModel, including "modifications" aka variations (different)
        - dsWriteSolveFile
        - run solve_file
        - get data
- see paper fig 9 for code flow
- have to start SOMEWHERE, not with all funcs of all of DS

### seem to be at least 2 problems for the "fast kinetic syns" of Des 1994
- R depends on previous versions of itself in time, and everyway i try this it
  complains that there's an unresolvable cycle
- need to refer to previous versions of value. B2 seems well-equipped to handle
  calculating time differences e.g. between (t-lastupdate), but I can't find
  any examples of using these time differences in ORDER to grab a previous
  value of something like R. (additionally, can't seem to get even something
  like "v_pre(t)" to work)
- kind of similarly, marcel's response to jenny is pretty equivalent (in fact
  more complex?) than our tanh version, and probably just as computationally
  expensive since you need to solve an ODE at every time step
- conclusion on attempting to implement the Fast Kinetic Destexhe synaptic
  methods in brian2 as of 20180202: even if this is possible in B2, which I'm
  not sure it is, it'll take far more understanding of B2 than I have. Not to
  mention, we already have a working Tanh style that definitely works.

### https://github.com/JoErNanO/brianmodel

### should separate the independent parallel distribution / writing complete code files as an independent module

### singularity containers?

### todos from code
- from Model.py
    - move this to org mode, and make a SCRIPT just for testing and plotting
      any hidden normxn of brian – AND make a DynaSim simulation for direct
      comparison!!!
    - TBH, this is a "nice to have" it's NOT necessary, since even with
      stochastic connections, can still estimate normalization denominator
      (actually this is wrong see below)
    - actually, stochastic case is NOT easy since the postsyn cell is going to
      see VERY diff activity from 1 strong cxn to 1 cell compared to 10% strong
      connection from 10 cells
    - in other words, the "signal" the postsyn will see will be very diff b/w
      those two cases
    - "solution" in this case could still be "figure it out yourself"
    - the only is to see if B2 auto-adds ANY kind of normalization of the below
      four cases. if not, then can let user do it, since any of these sitns can
      be done by user
    - this means need to experiment with sAMPAtotal, connection #'s, and
      current - try using small 2x2 network
    - realtalk: i'm thinking about four different situations, and only number 2
      and # 4 are likely "correct". Also, ONLY thing that matters is how many
      source cells any target cell is receiving from
    - stochastic cxn chance and every target cell receives from 10ish source
      cells, but each cxn adds an "entire g_max", so the target cell may
      experience a simulatneous IAMPA of the 1, 2, or N*g_max
    - this requires no normxn , can simply have a stochastic connection_eqns
      and throw a "g" in the mech
    - note: i'm pretty sure this is NOT the model used by most/all HH syn
      modeling, since would results in 10x g_max into target
    - stochastic cxn chance and every target cell receives from 10ish source
      cells, but all cxns' currents together add up to a single unit of
      scaled-down/normalized
    - g_max, so each INDIVIDUAL presyn spike doesn't strongly affect the target
      cell (but in aggregate, may reach g_max)
    - this reqs normxn, but isn't this completely solved by just dividing ALL
      g_max's by 10 (or whatever 1/("how many source cells is each target cell
      receiving from on avg") is)?
    - simpler implementation: "g_max / (N_pre * cxn_prob)" so if 100 source
      popn size and 10% prob in connection_eqns, on avg each target will
      receive 10 syns of g_max/10, adding up to 1 g_max
    - note: i'm pretty sure this IS the model used by most/all HH syn modeling,
      in that g_max is the COMPLETE amount of charge from ALL syns of a single
      type
    - fixed cxns e.g. 10-cell cxn diameter
    - means you still have to think about "how many src cells is each target
      receiving from"
    - each target will see a convolution pass, so will have 10 src cells
    - fixed all-to-all => each target will receivee from all source, so divide
      by N_pre
    - weights do not have to be binary, but i'm not messnig with non-binary
      weeights
    - test to see if summed variables DO scale properly, using "full model"
    - wrong, needs to be the ACTUAL number of source neurons, which depends on
      the 'connection_eqns'
    - can use self.synapses[index][mechanism]['synapse_object'].target._N for
      total size
    - BUT if have to initially build dummy Synapse object in order to set
      source number (in order to
    - normalize syns when ACTUALLY building synapse object and making
      equations), then have to delete
    - that synapse object after building
    - could either 1 compute it automagically by building intermediate? synapse
      object with 'connection_eqns' or 2 let user do it like with DS
    - try, from Synapses object documentation, "_registeredvariables : Set of
      Variable objects that should be resized when the number of synapses
      changes"
    - seems can get at least initial cell #'s of source and target sizes via
      self.synapses[index][mechanism]['synapse_object'].variables._variables['N_incoming'].size
      or
      self.synapses[index][mechanism]['synapse_object'].variables['N_incoming'].size
      using this and other possible variables 'N_outgoing', '_targetoffset' and
      '_sourceoffset', '_presynapticidx' and '_postsynapticidx'
    - The problem is that none of these seem to have processed the connect
      condition (that each should only be connected to at a radius of 5)
- from model iGABAa.mech
    - check YAML colons work
    - what if two different GABAa currents onto same cell? 'target_neuron' vars
      may need to be customized for that connection, BUT the related "s_post"
      var in the synapse will need to be as well
        - could prefix all with
    - p 123, can substite at read in a la `=Equations(eqns, g='g_RETCGABAa',
      tau='tau_RETCGABAa')`
        - ugh that means that outcoming things like 'I_RETCGABAa' will be ugly,
          but then they can be prog'd?
        - ugh what about underscores then? – if just adding to string, then not
          a problem, likely only a problem upon analysis time
        - another problem: the _post var
- from models/iGABAa.yaml

## planning

### start building dynasimpy interface off of dynasim interface, wrap
dsSimulate around pypet wrapper around brian2 caller

### it's def too much to ask people to learn pypet, needs to be trivial

### experimental writeup of plan interface 20171221 (thinking out loud)
- mechanism files
- parameter variation possibilities
    - "parameters" python package
        - from sumatra developers?
          <https://github.com/NeuralEnsemble/parameters/>
        - has support for units, but NOT like Brian
        - in fact, Brian2 units may interfere with Parameters package
        - Parameters places much emphasis on enabling dot notation of
          parameters, but IIRC B2 has somoething like this almost out of the
          box
    - pscan <https://pypi.python.org/pypi/pscan/1.0.0>
        - agree with this thinking: The impetus for the design of the module
          was the realization that there are basically only four types of
          “parameter sweeps” that ever really need to be done.
            - run the same parameters many times (e.g. stoch simulation)
            - vary certain parameters jointly (e.g. (i,j) = (1,2), (2,3),
              (3,4), ... )
            - vary parameters combinatorially (e.g. (i,j) = (1,1), (1,2),
              (2,1), (2,2))
            - vary “scientifically” (e.g. (i0,j),(i,j0) for fixed i0,j0,
              varying i,j)
    - sciexp2 !!! this seems closest to out-of-the-box dynasim batch
      distribution
        - has "translators"/translation for programming string writing? like
          reproducible code?
        - actually, more than just C-like, seems to assume you're going to pass
          in your parameters via the SHELL, NOT a param file
        - unfortunately, may be more complex than worth
    - by hand
- individual full simulation charxn
    - would wrapping in an individual pypet traj (single point) enable easy
      multicore?
        - pypet "multiprocessing" analgous to dynasim "sims_perjob"
            - makes notes about how openBLAS is not well supported, and issues
              with multithreading can get complicated
            - also requires data to be pickled, which also really screws with
              multithreading?
            - ugh BUT if main parallel model is saving every sime to different
              hdf5, then this may be incompatible
            - also "HDF5 is not thread-safe"
        - conclusion of all these points is...yes, but there's a lot of catches
          (esp that HDF5 not thread safe): leave multiproc for v2
    - sciexp2? might need more library-specific charxn than desired
        - also, pypet supports brian2 units
        - also, pypet sort of built to work with brian2, so can expect
          interface to be somewhat functionable
        - seems to be built around raw parameter files as inputs to your main
          program
            - dynasim model is NOT a call to dsSimulate, but rather a "solve"
              file that has parameters embedded in single file
            - what we're talking about here is the difference b/w
                - DS writing its complete own solve file (meaning saving a
                  completely self-contained, reproducible version of this
                  specific simulation, one that is NOT similar to any other DS
                  interface)
                - 2. just passing a parameter file to a common DP, and
                - 3. compiling every brian2 simulation
                    - ironically, this may be technically more reproducible
                      than option 2
        - uses its own data model similar to numpy NDarrays?
            - prob don't have to use dat amodel
        - really built more for every-simulation-compiled C-like programs, even
          though parallelization model is like ours
        - actually, more than just C-like, seems to assume you're going to pass
          in your parameters via the SHELL, NOT a param file
    - param file?
        - how is this different than the dsSimulate interface?
        - needs to be able to arbitrarily add values of any existing parameter
            - write checker to make sure that all inputted params pre-exist in
              the model neurons/syns
            - after, write checker for if inputted params are same units as
              preexisting params
        - units? thankfully, any list can just by multiplied by its unit
        - oh jesus, need to be able to parametrize by population (NeuronGroup),
          connection (Synapse)
            - what is the internal memory model of identically named parameters
              for mechanisms (e.g. gNa for two different mechanisms)? or is
              this unsupported in DS as well
                - actually may not matter, since probably end up using dot
                  notation
            - i.e. uniquely identify where params go
        - due to units, either
            - needs to be valid python code (requiring function def), or
                - (keep in mind that DS params don't work from CLI either)
                - need to be able to add comments!
            - valid yaml/json using NUMBERS where units are indicated by
              SEPARATE strings, or
            - valid yaml/json where all params are strings that are executed
        - alternatively, could disable unit checking in brian2 since ALL
          parametrization and parameter tracking is more difficult without it
        - however, units are processed by pypet and param files/sweeps could be
          generated using pypet IF they could be liberated into individual sims
            - note: how well do pypet units work when using sumatra?
        - how to handle brian2 units with sumatra parameters?
    - what about, if cluster_flag, just have pypet "main program" be running
      individualized scripts instead of B2 itself?
- batch submission possibilities
    - scoop
    - slurm
    - saga seems easiest, BUT requires 2.7??? wtf
    - raw dynasim
- metadata and provenance tracking
    - at minimum want to use sumatra, since offers a LOT of possibilities
- data storage: hdf5?
    - SQL would be asking too much of end users
    - each job gets its own hdf5?
        - pros: like dynasim, easiest to intuitively understand
        - cons: want data format to be consistent and backwards-compatible
- post hoc analysis
    - <https://pypi.python.org/pypi/pyGTC>
    - gimblvis

### Need to draw out the json payload, control flow, how it works with entire
system and especially batch system

### E.g. how to apply namespace before NGs are instantiated, or at time of?
Need to take a step back and reorg so that not constructing NGs etc so fast

### Vary applied differently than regular params? Keep in mind the only thing
that matters is error prevention, which any equation checking should check.

### Also consider that changing namespace post hoc is MUCH easier using Brian
interface than before. Only assumption is that parameter name changes are
consistent.

### To keep separate from properly name spaced eqns, should just pass
parameters/vary to json as separate dict in json. Uniqify?

### Where json payload is individualized depends on parallel method used. Maybe
separate identical "model.json" from small "custom_parameters.json" in
batchdirs, but ONLY if copying 5000 individualized "model.json" files takes too
long

## notes on python packaging

## data format

### HDF5 justification, read lrn

### Store most data as pandas and metadata in single tree

### NSDF is clear and self-explanatory, but main library for it doesn't have
python3 compatibility! <https://github.com/nsdf/nsdf/issues/42>

### notes on Sonata
- conclusion: too complex to use at this time
    - meant to subsume lower-level formats, e.g. supports inclusion of NeuroML
      model spec
    - uses several different filetypes for several different purposes
    - wait where is the data stored???
- mention in their requirements that they specifically need multiple read AND
  write
    - can maybe only happen with multiple HDF5 files, which almost defeats the
      point of HDF
- uses nodes for cells and edges for syns/juncs
- mentions focus on efficiency and compactness
- from the "SONATA developer guide"
    - "leveraging HDF5 and SQLite, graph dbs, spatial indexing"
    - representing morphologies
        - uses SWC format from NeuroMorpho
        - (not self-describing?)
    - representing ion chnls, pt nrs, and syn mdls
        - "Neuron MOD files are used"
        - NeuroML/LEMS format for simulator independence "left for later date"
    - representing chnl dist and composition (incl params), 3 formats
      supported:
        - NeuroML XML - NeuroML v2 not yet fully supported
        - JSON Allen Cell Types DB schema
        - HOC
    - representing networks
        - "node types" in CSV (indexes the below)
        - separate population in HDF5's
        - most of format description is here
    - representing simulations
        - separate JSON file with sim params

## s6d2-destexhe synapses

- roughly destexhe syns ?
  <http://brian2.readthedocs.io/en/stable/examples/frompapers.Vogels_et_al_2011.html>
- (20180803) can transform [T](Vpre) = Tmax / (1 + exp(-(Vpre-Vp)/Kp)) where Vp
  is half-activation (e.g. 2 mV) and Kp is "steepness" (e.g. 5 mV) from
  http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.164.9768&rep=rep1&type=pdf
    - used in wang rinzel 1992
    - for slow, "ligand-gated channels" like NMDA and GABAB, will still need
      ODEs
    - from Theoretical Neuroscience: "Figure 5.14 shows a fit to a recorded
      postsynaptic current using this for- malism. In this case, βs was set to
      0.19 ms−1 . The transmitter concentra- tion was modeled as a square pulse
      of duration T = 1 ms during which αs = 0.93 ms−1 . Inverting these
      values, we find that the time constant de- termining the rapid rise seen
      in figure 5.14A is 0.9 ms, while the fall of the current is an
      exponential with a time constant of 5.26 ms."
    - "beta/channel closing usu much larger than alpha/channel opening"

- for minis try PoissonInput
  https://brian2.readthedocs.io/en/stable/reference/brian2.input.poissoninput.PoissonInput.html
- TODO after implement destexhe-style, upload example code for brian2 website

## s6d3 figure out thresholds

### are "event-driven" syns computed at all once the threshold is no longer
satisfied, or are they "canceled"/"emptied"?

### threshold seems to be a yes/no thing right now - can the "events" be
"triggered" by threshold crossings, rather than time spent above the threshold
itself?

### maybe instead of only wanting to calc upon thresh crossing, should only
trigger just when satisfying thresh (above 0), since 1. tanh anyway, 2. STILL
want clock-driven calc WHEN thresh is crossed

### there is a separate issue/typo/bug about why is sAMPAtotal going off ALL
the time with the threshold???

## Pynasim is CURRENTLY ON HOLD until AFTER grad school

### reasons to do DynaSim in remaining gs time over PynaSim/a Brian2 interface
- hell would probably freeze over before Nancy would even consider letting me
    - do things in a language I'm only a beginner in and
    - build yet ANOTHER system (almost) from scratch that no one else in the
      lab has experience programming in – she would not even remotely care
      about FOSS rights enough to rewrite something that already "works"
    - this means i would also have to keep it from the LAB, since she would
      hate it so much she would be made if she even HEARD that I was doing it
      from someone else
- most importantly, making DynaSim nice is more SELLABLE to employers of a
  potential postdoc, even/especially to people who value FOSS or software
- subpoint: even if I switched to creating PynaSim, I'm not sure I would A.
  learn enough to call myself proficient in Python (unlike DS ->MATLAB) B. have
  enough time to create a satisfying 1.0 release, AND learn the lang, AND learn
  the tools etc. C. it's probably better to advertise strong strength in MATLAB
  alongside a decent 1.0 project, instead of okay strength in MATLAB and Python
  but only in multiple meh 0.5 projects — this would still be true prob for
  FOSS postdocs
- if anything, switching FROM a "collab" project to doing one in isolation
  would beg the question why i wasn't collab, meanwhile doing actual dev on DS
  DEFINITELY counts for working on a "decently sized software project
  collaboratively with the lab"
- importantly, if my name is on DS but I don't improve it (and merely claim
  that I contributed ideas/architecture), then I may get blamed for its
  architecture and messiness in the code organization and lack of docs - it
  becomes a liability to anyone who knows code and looks into it (though
  chances of such inspection are low)
- I don't need to give it every feature ever, instead I can just work to make
  it GOOD ENOUGH
- i can practice doing it the "professional" way on github via fetch and pull
  requests
- i can sell it as collab and that i helped organize the lab to work with it,
  even though it's really just me and jason and maybe salva
- would be more of an asset to other lab people, and better xp with the system
  means i may be able to help people port their analysis
10. i'd have tons of dev freedom, since not many are interested in serious dev
    work on it

### conclusion: for rest of gs, it's better from a CAREER perspective to make
DS good enough / 1.0 with good docs, than it is to go on my own, alone and in
isolation, and even in stealth mode

## thoughts

### Start python implementation of dnsim for github resume

### make 100% compatible with mechanism files for ease of transfer (can always
optimize after the fact, though they're already ****simple**** which is good)

### to use DynaSim at scale where it shines, not only need hardware no matter
what system, but need LOTS of matlab licenses, not just one!!! WE had problems
with matlab licenses in the first few years of dynasim use ourselves!!!!

## thinking 20160804, after looking at Brian2 (beta rc3) docs

### pros over dynasim (i.e. switching "core" to brian2 instead of dynasim)
- b2 is MUCH more mature, both in code org and docs – this includes the
  negative that it's more complex/larger
- is under active development by at least several people, up to 10 – and is
  making progress
- lofty goals include GPU stuff, export to other systems (already has data
  export to pandas), etc.
- the "engine" is probably more powerful (i.e. can add complicated inputs with
  less bugs)
- competitively fast, if not faster – and they're working on speed
- already working on Docker installs for even easier deployment

### instead of just switching DynaSim "engine" to Brian2, after looking at
NeuralEnsemble tools and Brian2 docs, it seems like it would be better in the
long-run to "join the Brian2 community"
- I no longer think it's a good idea to use the identical Mechanism files from
  Dynasim, although adapted mechanism files would have the same complexity
- specifying the model etc. is also the same level of complexity
- code-wise what is needed for Brian2 equivalence is
    - parametrization (could follow dynasim process)
    - data handling (json metadata + csv? not to mention simple hdf5 + NWB
      hdf5)
    - plotting/analysis (there are python neuro libs that could help, like
      Elephant <http://elephant.readthedocs.io/en/latest/overview.html>)

## future ideas
- use GNU parallel for local embarrassingly parallel jobs