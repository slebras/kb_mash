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


    /**
     * Pass in **one of** fasta_path, assembly_ref, or reads_ref
     *   fasta_path - string - local file path to an input fasta/fastq
     *   assembly_ref - string - workspace reference to an Assembly type
     *   reads_ref - string - workspace reference to a Reads type
     */
    typedef structure {
        string fasta_path;
        string assembly_ref;
        string reads_ref;
    } MashSketchParams;

    /**
     * Returns the local scratch file path of the generated sketch file.
     * Will have the extension '.msh'
     */
    typedef structure {
        string sketch_path;
    } MashSketchResults;

    /**
     * Generate a sketch file from a fasta/fastq file
     */
    funcdef run_mash_sketch(MashSketchParams params)
        returns(MashSketchResults results) authentication required;
};
