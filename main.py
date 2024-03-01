import streamlit as st

from helper_functions import load_data_from_github, filter_data, plot_data_subplots, get_galaxy_names, \
								spectral_lines, extract_lines_and_wavelengths, plot_data_subplots_split #load_data

with st.sidebar:
	sel_options = st.radio("Select Options", ['Galaxy Spectra', 'References'])



if sel_options == "Galaxy Spectra":
	st.header("Galaxy Spectra")


	# local
	#directory = './Data/Figure_1'
	#data_dict_all = load_data(directory)

	
	data_dict_all = load_data_from_github()
	#st.write(data_dict_all)
	#st.write(data_dict)

	with st.sidebar:
		variability = st.radio("Sample", ("Full Sample", "Variable", "Non Variable"))
		
	if variability == "Full sample":
		st.write("[Clark et al. (2024)](https://academic.oup.com/mnras/article/528/4/7076/7609067?login=false) presents 'new spectroscopic and photometric \
			follow-up observations of the known sample of extreme coronal line-emitting galaxies (ECLEs) identified in the Sloan Digital Sky Survey (SDSS).'")

	if variability == "Variable":
		st.write("Galaxies from the [Clark et al. (2024)](https://academic.oup.com/mnras/article/528/4/7076/7609067?login=false) that show spectral variability - \
			in particular of the coronal Fe lines – over the observation period. SDSS J1241 was originally classified as non-variable by [Yang et al. (2013)](https://iopscience.iop.org/article/10.1088/0004-637X/774/1/46),\
			 but shown to be variable by [Clark et al. (2024)](https://academic.oup.com/mnras/article/528/4/7076/7609067?login=false) observations.")

	if variability == "Non Variable":
		st.write("Galaxies from the [Clark et al. (2024)](https://academic.oup.com/mnras/article/528/4/7076/7609067?login=false) that do not show spectral variability - \
			in particular of the coronal Fe lines – over the observation period.")

	data_dict = filter_data(data_dict_all, variability)
	galaxy_names = get_galaxy_names(data_dict)
	with st.sidebar:
		individual_galaxies = st.selectbox("Individual Galaxies", list(set(galaxy_names)), index=None)

	if individual_galaxies:
	    selected_galaxies = individual_galaxies

	    #multiselect
	    #selected_keys = [key for key in data_dict.keys() for galaxy in selected_galaxies if key.startswith(galaxy)]
	    #selectbox
	    selected_keys = [key for key in data_dict.keys() if key.startswith(selected_galaxies)]

	    data_dict = {key: data_dict[key] for key in selected_keys}


	# Filter data_dict based on selected galaxies
	filtered_data_dict = data_dict # {key: df for key, df in data_dict.items() if any(key.startswith(galaxy_name) for galaxy_name in sel_gal)}


	with st.sidebar:
		show_lines = st.radio("Show spectral lines", ('No lines', 'All lines', 'Selected lines'))

		if show_lines == "All lines":
			lines_with_wavelengths = spectral_lines()

			lines, wavelengths = extract_lines_and_wavelengths(lines_with_wavelengths)

		if show_lines == "Selected lines":
			st_lines = st.multiselect("Select lines to plot", ['[FeVII]', 'Hδ', 'HeI', 'HeII', 'Hβ', '[OIII]', '[FeXIV]', '[FeX]', 'Hα', '[FeXI]'])
			lines_with_wavelengths = spectral_lines()
			lines_with_wavelengths = {line: wavelength for line, wavelength in lines_with_wavelengths.items() if line in st_lines}

			lines, wavelengths = extract_lines_and_wavelengths(lines_with_wavelengths)


		if show_lines == 'No lines':
			lines = None
			wavelengths = None


	with st.sidebar:

		if individual_galaxies:
			display = "Single"
		else:
			display = st.radio("Display Graphs", ('Single', 'Subplots'))

	if display == 'Single':
		#if variability == "Variable":
		#	fig = plot_data_subplots(filtered_data_dict, "Single", "Variable", lines=lines, wavelengths=wavelengths)

		if individual_galaxies:
			fig = plot_data_subplots(filtered_data_dict, "Single", selected_galaxies, lines=lines, wavelengths=wavelengths)
		else:
			fig = plot_data_subplots(filtered_data_dict, "All", lines=lines, wavelengths=wavelengths)
		
		if variability == "Variable":
			fig = plot_data_subplots(filtered_data_dict, "Single", "Variable", lines=lines, wavelengths=wavelengths)

			if individual_galaxies:
				fig = plot_data_subplots(filtered_data_dict, "Single", selected_galaxies, lines=lines, wavelengths=wavelengths)

		if variability == "Non Variable":
			fig = plot_data_subplots(filtered_data_dict, "Single", "Non Variable", lines=lines, wavelengths=wavelengths)
			if individual_galaxies:
				fig = plot_data_subplots(filtered_data_dict, "Single", selected_galaxies, lines=lines, wavelengths=wavelengths)

	if display == "Subplots":
		#

		if variability == "Variable":
			fig = plot_data_subplots_split(filtered_data_dict, "Variable", lines=lines, wavelengths=wavelengths)
		if variability == "Non Variable":
			fig = plot_data_subplots_split(filtered_data_dict, "Non Variable", lines=lines, wavelengths=wavelengths)

		else:
			fig = plot_data_subplots_split(filtered_data_dict, "Individual", lines=lines, wavelengths=wavelengths)
		


	st.plotly_chart(fig, use_container_width=True, height=800)


#if sel_options == "AGNs":
#	st.write("AGN data from [Clark et al. (2024)](https://academic.oup.com/mnras/article/528/4/7076/7609067?login=false):")


if sel_options == "References":
	st.header("References")
	st.write(
		"""Based on the research by [Clark et al. (2024)](https://academic.oup.com/mnras/article/528/4/7076/7609067?login=false)
	""")

	st.write("Spectral sequences showing the original SDSS spectra (black) for each ECLE along with the corresponding MMT follow-up spectrum obtained by\
	 [Yang et al. (2013; blue)](https://iopscience.iop.org/article/10.1088/0004-637X/774/1/46) \
		and the new follow-up spectra obtained through work by Clark et al (other colours depending on source).")
	st.write("")
	st.write(""" 
		Data made publicly accessible via Zenodo by [Clark et al. (2024)](https://zenodo.org/records/10635862)
		""")
	st.write("")

	st.write(""" 
		This Streamlit application is made by SciStreams, code of the app can be found on [**GitHub**](https://github.com/SciStreams/ECLE_galaxies_streamlit).
		""")
	st.write("")
	st.write("If you find ECLEs useful in your research, please cite original paper:")
	st.code(""" 

@ARTICLE{2024MNRAS.tmp..536C,
       author = {{Clark}, Peter and {Graur}, Or and {Callow}, Joseph and {Aguilar}, Jessica and {Ahlen}, Steven and {Anderson}, Joseph P. and {Berger}, Edo and {M{\"u}ller-Bravo}, Tom{\'a}s E. and {Brink}, Thomas G. and {Brooks}, David and {Chen}, Ting-Wan and {Claybaugh}, Todd and {de la Macorra}, Axel and {Doel}, Peter and {Filippenko}, Alexei V. and {Forero-Romero}, Jamie E. and {Gomez}, Sebastian and {Gromadzki}, Mariusz and {Honscheid}, Klaus and {Inserra}, Cosimo and {Kisner}, Theodore and {Landriau}, Martin and {Makrygianni}, Lydia and {Manera}, Marc and {Meisner}, Aaron and {Miquel}, Ramon and {Moustakas}, John and {Nicholl}, Matt and {Nie}, Jundan and {Onori}, Francesca and {Palmese}, Antonella and {Poppett}, Claire and {Reynolds}, Thomas and {Rezaie}, Mehdi and {Rossi}, Graziano and {Sanchez}, Eusebio and {Schubnell}, Michael and {Tarl{\'e}}, Gregory and {Weaver}, Benjamin A. and {Wevers}, Thomas and {Young}, David R. and {Zheng}, WeiKang and {Zhou}, Zhimin},
        title = "{Long-term follow-up observations of extreme coronal line emitting galaxies}",
      journal = {\mnras},
     keywords = {transients: tidal disruption events, galaxies: active, Astrophysics - High Energy Astrophysical Phenomena},
         year = 2024,
        month = feb,
          doi = {10.1093/mnras/stae460},
archivePrefix = {arXiv},
       eprint = {2307.03182},
 primaryClass = {astro-ph.HE},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2024MNRAS.tmp..536C},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}

			""")


with st.sidebar:
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")

	st.sidebar.info(
		"""This Streamlit app showcase examples from research paper "Long-term follow-up observations of extreme coronal line emitting galaxies".
		Read research paper by [Clark et al. (2024)](https://academic.oup.com/mnras/article/528/4/7076/7609067?login=false)
		"""
		)


	col1, col2 = st.columns([0.7,0.2])
	with col1:

		st.markdown('''
	    <a href="https://scistreams.github.io">
	        <img src="https://scistreams.github.io/images/SciStreams.png" width="150" />
	    </a>''',
	    unsafe_allow_html=True
		)
		st.markdown('App made by [**SciStreams**](https://scistreams.github.io/)')