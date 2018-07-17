
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
 * * Pass in **one of** fasta_path, assembly_ref, or reads_ref
 * *   fasta_path - string - local file path to an input fasta/fastq
 * *   assembly_ref - string - workspace reference to an Assembly type
 * *   reads_ref - string - workspace reference to a Reads type
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "fasta_path",
    "assembly_ref",
    "reads_ref"
})
public class MashSketchParams {

    @JsonProperty("fasta_path")
    private String fastaPath;
    @JsonProperty("assembly_ref")
    private String assemblyRef;
    @JsonProperty("reads_ref")
    private String readsRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("fasta_path")
    public String getFastaPath() {
        return fastaPath;
    }

    @JsonProperty("fasta_path")
    public void setFastaPath(String fastaPath) {
        this.fastaPath = fastaPath;
    }

    public MashSketchParams withFastaPath(String fastaPath) {
        this.fastaPath = fastaPath;
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
        return ((((((((("MashSketchParams"+" [fastaPath=")+ fastaPath)+", assemblyRef=")+ assemblyRef)+", readsRef=")+ readsRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
