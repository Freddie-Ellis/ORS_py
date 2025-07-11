def extract_setups(LSD_CD_results, LSD_CL_results, LSD_CLF_results, LSD_CLR_results):
    def extract_setup(data):
        print(data[0][0][1])
        return [
            [
                x['all_info'].hRideSetupF,
                x['all_info'].hRideStaticR,
                x['all_info'].xBumpGapSetupFM,
                x['all_info'].Component2_value,
                x['all_info'].slice_value
            ]
            for x in data
        ]

    setupList_CD = extract_setup(LSD_CD_results)
    setupList_CL = extract_setup(LSD_CL_results)
    setupList_CLF = extract_setup(LSD_CLF_results)
    setupList_CLR = extract_setup(LSD_CLR_results)

    return setupList_CD, setupList_CL, setupList_CLF, setupList_CLR
