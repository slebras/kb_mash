
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
 * <p>Original spec-file type: MashSketchResults</p>
 * <pre>
 * *
 * * Returns the local scratch file path of the generated sketch file.
 * * Will have the extension '.msh'
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "sketch_path"
})
public class MashSketchResults {

    @JsonProperty("sketch_path")
    private String sketchPath;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("sketch_path")
    public String getSketchPath() {
        return sketchPath;
    }

    @JsonProperty("sketch_path")
    public void setSketchPath(String sketchPath) {
        this.sketchPath = sketchPath;
    }

    public MashSketchResults withSketchPath(String sketchPath) {
        this.sketchPath = sketchPath;
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
        return ((((("MashSketchResults"+" [sketchPath=")+ sketchPath)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
