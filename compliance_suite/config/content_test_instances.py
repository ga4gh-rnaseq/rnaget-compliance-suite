import compliance_suite.functions.content_testing as cf

EXPRESSION_VALUE_1 = {
    "function": cf.expression_value_test_case,
    "name": "Expression Value 1",
    "i": {
        "r": 38,
        "c": 8
    },
    "o": {
        "GeneID": "ENSG00000206549",
        "GeneName": "PRSS50",
        "Condition": "bladder transitional cell carcinoma",
        "Tissue": "urinary bladder",
        "Sample": "DO472 - primary tumour",
        "Value": 0.0
    }
}

EXPRESSION_VALUE_2 = {
    "function": cf.expression_value_test_case,
    "name": "Expression Value 2",
    "i": {
        "r": 68,
        "c": 15
    },
    "o": {
        "GeneID": "ENSG00000239589",
        "GeneName": "LINC00879",
        "Condition": "breast adenocarcinoma",
        "Tissue": "breast",
        "Sample": "DO44273 - primary tumour",
        "Value": 0.0
    }
}

EXPRESSION_VALUE_3 = {
    "function": cf.expression_value_test_case,
    "name": "Expression Value 3",
    "i": {
        "r": 47,
        "c": 70
    },
    "o": {
        "GeneID": "ENSG00000223273",
        "GeneName": "RN7SKP172",
        "Condition": "melanoma",
        "Tissue": "skin",
        "Sample": "DO37946 - metastatic tumour",
        "Value": 0.0
    }
}

EXPRESSION_VALUE_4 = {
    "function": cf.expression_value_test_case,
    "name": "Expression Value 4",
    "i": {
        "r": 3,
        "c": 38
    },
    "o": {
        "GeneID": "ENSG00000084693",
        "GeneName": "AGBL5",
        "Condition": "endometrial adenocarcinoma",
        "Tissue": "uterus",
        "Sample": "DO43811 - primary tumour",
        "Value": 50.0
    }
}

EXPRESSION_VALUE_5 = {
    "function": cf.expression_value_test_case,
    "name": "Expression Value 5",
    "i": {
        "r": 30,
        "c": 92
    },
    "o": {
        "GeneID": "ENSG00000186501",
        "GeneName": "TMEM222",
        "Condition": "renal cell carcinoma",
        "Tissue": "kidney",
        "Sample": "DO46856 - normal",
        "Value": 16.0
    }
}

EXPRESSION_VALUE_6 = {
    "function": cf.expression_value_test_case,
    "name": "Expression Value 6",
    "i": {
        "r": 83,
        "c": 74
    },
    "o": {
        "GeneID": "ENSG00000255543",
        "GeneName": "AP005597.4",
        "Condition": "ovarian adenocarcinoma",
        "Tissue": "ovary",
        "Sample": "DO46366 - primary tumour",
        "Value": 0.0
    }
}

EXPRESSION_VALUE_7 = {
    "function": cf.expression_value_test_case,
    "name": "Expression Value 7",
    "i": {
        "r": 52,
        "c": 9
    },
    "o": {
        "GeneID": "ENSG00000227172",
        "GeneName": "AC011290.1",
        "Condition": "bladder transitional cell carcinoma",
        "Tissue": "urinary bladder",
        "Sample": "DO561 - primary tumour",
        "Value": 0.7
    }
}

EXPRESSION_VALUE_8 = {
    "function": cf.expression_value_test_case,
    "name": "Expression Value 8",
    "i": {
        "r": 31,
        "c": 89
    },
    "o": {
        "GeneID": "ENSG00000188763",
        "GeneName": "FZD9",
        "Condition": "renal cell carcinoma",
        "Tissue": "kidney",
        "Sample": "DO20604 - primary tumour",
        "Value": 0.4
    }
}

EXPRESSION_VALUE_9 = {
    "function": cf.expression_value_test_case,
    "name": "Expression Value 9",
    "i": {
        "r": 82,
        "c": 13
    },
    "o": {
        "GeneID": "ENSG00000254946",
        "GeneName": "AC073172.2",
        "Condition": "breast adenocarcinoma",
        "Tissue": "breast",
        "Sample": "DO2995 - primary tumour",
        "Value": 0.0
    }
}

EXPRESSION_VALUE_10 = {
    "function": cf.expression_value_test_case,
    "name": "Expression Value 10",
    "i": {
        "r": 95,
        "c": 93
    },
    "o": {
        "GeneID": "ENSG00000266172",
        "GeneName": "ENSG00000266172",
        "Condition": "renal cell carcinoma",
        "Tissue": "kidney",
        "Sample": "DO46909 - primary tumour",
        "Value": 0.0
    }
}

EXPRESSION_SLICE_1 = {
    "function": cf.expression_slice_test_case,
    "name": "Slice by featureIDList",
    "featureIDList": [
        "ENSG00000037965", "ENSG00000243503", "ENSG00000259285"
    ]
}

EXPRESSION_SLICE_2 = {
    "function": cf.expression_slice_test_case,
    "name": "Slice by featureNameList",
    "featureNameList": [
        "PGLYRP3", "PRSS50", "SNRPFP1", "OR5AC4P",
        "CLIC1", "RF00092", "AC100827.4"
    ],
}

EXPRESSION_SLICE_3 = {
    "function": cf.expression_slice_test_case,
    "name": "Slice by sampleIDList",
    "sampleIDList": [
        "DO22935 - primary tumour", "DO20604 - primary tumour",
        "DO48516 - primary tumour", "DO42881 - primary tumour",
        "DO6144 - primary tumour", "DO40948 - primary tumour",
        "DO472 - primary tumour", "DO48505 - primary tumour"
    ]
}

EXPRESSION_SLICE_4 = {
    "function": cf.expression_slice_test_case,
    "name": "slice by featureIDList and sampleIDList",
    "featureIDList": [
        "ENSG00000106278", "ENSG00000142025", "ENSG00000171487",
        "ENSG00000184471", "ENSG00000213719", "ENSG00000239589"
    ],
    "sampleIDList": [
        "DO52655 - primary tumour", "DO52685 - primary tumour",
        "DO25887 - primary tumour",
    ]
}

EXPRESSION_SLICE_5 = {
    "function": cf.expression_slice_test_case,
    "name": "slice by featureNameList and sampleIDList",
    "featureNameList": [
        "SH3BP1", "APOL5", "RN7SL592P"
    ],
    "sampleIDList": [
        "DO1249 - primary tumour", "DO28763 - primary tumour", 
        "DO33408 - primary tumour", "DO219961 - primary tumour",
        "DO2995 - primary tumour", "DO18671 - primary tumour",
        "DO219106 - primary tumour"
    ]
}

CONTINUOUS_VALUE_1 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Value 1",
    "assert_values": [
        {
            "i": { # input to assertion function,
                "r": 1, # row
                "c": 20 # col
            },
            "o": { # output, or expected values
                "Track": "61729_test", # expected val at row 1
                "Position": "chr1:20",
                "Value": 8.904
            }
        }
    ]
}

CONTINUOUS_VALUE_2 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Value 2",
    "assert_values": [
        {
            "i": {
                "r": 0,
                "c": 5
            },
            "o": {
                "Track": "61721_test",
                "Position": "chr1:5",
                "Value": 6.205
            }           
        }
    ]
}

CONTINUOUS_VALUE_3 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Value 3",
    "assert_values": [
        {
            "i": {
                "r": 2,
                "c": 212
            },
            "o": {
                "Track": "61733_test",
                "Position": "chr5:143",
                "Value": 8.779
            } 
        }
    ]
}

CONTINUOUS_VALUE_4 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Value 4",
    "assert_values": [
        {
            "i": {
                "r": 3,
                "c": 159
            },
            "o": {
                "Track": "61737_test",
                "Position": "chr5:90",
                "Value": 24.704
            } 
        }
    ]
}

CONTINUOUS_VALUE_5 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Value 5",
    "assert_values": [
        {
            "i": {
                "r": 1,
                "c": 66
            },
            "o": {
                "Track": "61729_test",
                "Position": "chr1:66",
                "Value": 6.975
            } 
        }
    ]
}

CONTINUOUS_SLICE_1 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Slice by chr, 1",
    "chr": "chr1"
}

CONTINUOUS_SLICE_2 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Slice by chr, 2",
    "chr": "chr5"
}

CONTINUOUS_SLICE_3 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Slice by chr, start, 1",
    "chr": "chr1",
    "start": "32"
}

CONTINUOUS_SLICE_4 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Slice by chr, start, 2",
    "chr": "chr5",
    "start": "100"
}

CONTINUOUS_SLICE_5 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Slice by chr, end, 1",
    "chr": "chr1",
    "end": "22"
}

CONTINUOUS_SLICE_6 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Slice by chr, end, 2",
    "chr": "chr5",
    "end": "49"
}

CONTINUOUS_SLICE_7 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Slice by chr, start, end, 1",
    "chr": "chr1",
    "start": "30",
    "end": "50"
}

CONTINUOUS_SLICE_8 = {
    "function": cf.continuous_test_case,
    "name": "Continuous Slice by chr, start, end, 2",
    "chr": "chr5",
    "start": "69",
    "end": "117"
}





