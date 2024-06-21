from models.transformations.transform_data_for_models import DataTransformer

# function to use for when creating models.
####### NEEDS REFACTOR, SPECIALLY THE DF_TO_SUPERVISED. I'LL NEED TO THINK HOW TO MERGE DATA (DIFFERENT DATAFRAMES), ETC.
def transform_data_to_supervised(self):
    data_transformer = DataTransformer(window_size=5)
    for category, data_types in self.extracted_data_dict.items():
        # for data_type, data in data_types.items(): # todo: perform transformation on fundamental data too (once we have it)
        for name, df in data_types["technical"].items():
            self.transformed_data_dict[category]["technical"][
                name + "_transformed"
            ] = data_transformer.to_supervised(df)
