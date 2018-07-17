
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
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "fasta_path"
})
public class MashSketchParams {

    @JsonProperty("fasta_path")
    private String fastaPath;
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
        return ((((("MashSketchParams"+" [fastaPath=")+ fastaPath)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
