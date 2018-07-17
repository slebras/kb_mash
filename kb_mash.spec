/*
A KBase module: kb_mash
*/

module kb_mash {
    /*
        Insert your typespec information here.
    */


    typedef structure {
        string input_assembly_upa;
        string workspace_name;
        string search_db;
        int max_hits;
    } MashParams;

    typedef structure {
        string report_name;
        string report_ref;
    } MashResults;

    funcdef run_mash_dist_search(MashParams params)
        returns(MashResults results) authentication required;


    typedef structure {
        string fasta_path;
    } MashSketchParams;

    typedef structure {
        string sketch_path;
    } MashSketchResults;

    funcdef run_mash_sketch(MashSketchParams params)
        returns(MashSketchResults results) authentication required;
};
