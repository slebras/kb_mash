
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
    "workspace_name",
    "input_fasta_ref"
})
public class MashSketchParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_fasta_ref")
    private String inputFastaRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public MashSketchParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_fasta_ref")
    public String getInputFastaRef() {
        return inputFastaRef;
    }

    @JsonProperty("input_fasta_ref")
    public void setInputFastaRef(String inputFastaRef) {
        this.inputFastaRef = inputFastaRef;
    }

    public MashSketchParams withInputFastaRef(String inputFastaRef) {
        this.inputFastaRef = inputFastaRef;
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
        return ((((((("MashSketchParams"+" [workspaceName=")+ workspaceName)+", inputFastaRef=")+ inputFastaRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
