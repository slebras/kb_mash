
package us.kbase.kbmash;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: MashSketchParams</p>
 * <pre>
 * *
 * * Pass in **one of** input_path, assembly_ref, or reads_ref
 * *   input_path - string - local file path to an input fasta/fastq
 * *   assembly_ref - string - workspace reference to an Assembly type
 * *   reads_ref - string - workspace reference to a Reads type
 * * Optionally, pass in a boolean indicating whether you are using paired-end reads.
 * *   paired_ends - boolean - whether you are passing in paired ends
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_path",
    "assembly_ref",
    "reads_ref",
    "paired_ends"
})
public class MashSketchParams {

    @JsonProperty("input_path")
    private String inputPath;
    @JsonProperty("assembly_ref")
    private String assemblyRef;
    @JsonProperty("reads_ref")
    private String readsRef;
    @JsonProperty("paired_ends")
    private Long pairedEnds;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_path")
    public String getInputPath() {
        return inputPath;
    }

    @JsonProperty("input_path")
    public void setInputPath(String inputPath) {
        this.inputPath = inputPath;
    }

    public MashSketchParams withInputPath(String inputPath) {
        this.inputPath = inputPath;
        return this;
    }

    @JsonProperty("assembly_ref")
    public String getAssemblyRef() {
        return assemblyRef;
    }

    @JsonProperty("assembly_ref")
    public void setAssemblyRef(String assemblyRef) {
        this.assemblyRef = assemblyRef;
    }

    public MashSketchParams withAssemblyRef(String assemblyRef) {
        this.assemblyRef = assemblyRef;
        return this;
    }

    @JsonProperty("reads_ref")
    public String getReadsRef() {
        return readsRef;
    }

    @JsonProperty("reads_ref")
    public void setReadsRef(String readsRef) {
        this.readsRef = readsRef;
    }

    public MashSketchParams withReadsRef(String readsRef) {
        this.readsRef = readsRef;
        return this;
    }

    @JsonProperty("paired_ends")
    public Long getPairedEnds() {
        return pairedEnds;
    }

    @JsonProperty("paired_ends")
    public void setPairedEnds(Long pairedEnds) {
        this.pairedEnds = pairedEnds;
    }

    public MashSketchParams withPairedEnds(Long pairedEnds) {
        this.pairedEnds = pairedEnds;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((("MashSketchParams"+" [inputPath=")+ inputPath)+", assemblyRef=")+ assemblyRef)+", readsRef=")+ readsRef)+", pairedEnds=")+ pairedEnds)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
