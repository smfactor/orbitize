import orbitize.read_input
import orbitize.system
import orbitize.sampler

"""
This module reads input and constructs ``orbitize`` objects 
in a standardized way.
"""

class Driver(object):
    """
    Runs through ``orbitize`` methods in a standardized way.

    Args:
        filename (str): relative path to data file. See ``orbitize.read_input``
        sampler_str (str): algorithm to use for orbit computation. "MCMC" for 
            Markov Chain Monte Carlo, "OFTI" for Orbits for the Impatient
        num_secondary_bodies (int): number of secondary bodies in the system. 
            Should be at least 1.
        system_mass (float): mean total mass of the system [M_sol]
        plx (float): mean parallax of the system [mas]
        mass_err (float, optional): uncertainty on ``system_mass`` [M_sol]
        plx_err (float, optional): uncertainty on ``plx`` [mas]
        lnlike (str, optional): name of function in ``orbitize.lnlike`` that will
            be used to compute likelihood. (default="chi2_lnlike")
        mcmc_kwargs (dict, optional): ``num_temps``, ``num_walkers``, and ``num_threads`` 
            kwargs for ``orbitize.sampler.MCMC``

    Written: Sarah Blunt, 2018
    """
    def __init__(self, filename, sampler_str,
                 num_secondary_bodies, system_mass, plx, 
                 mass_err=0, plx_err=0, lnlike='chi2_lnlike', mcmc_kwargs=None):

        # Read in data
        data_table = orbitize.read_input.read_formatted_file(filename)

        # Initialize System object which stores data & sets priors
        self.system = orbitize.system.System(
            num_secondary_bodies, data_table, system_mass, 
            plx, mass_err=mass_err, plx_err=plx_err
        )

        # Initialize Sampler object, which stores information about
        # the likelihood function & the algorithm used to generate
        # orbits, and has System object as an attribute.
        if mcmc_kwargs is not None and sampler_str == 'MCMC':
            kwargs = mcmc_kwargs
        else:
            kwargs = {}

        sampler_func = getattr(orbitize.sampler, sampler_str)
        self.sampler = sampler_func(self.system, like=lnlike, **kwargs)
