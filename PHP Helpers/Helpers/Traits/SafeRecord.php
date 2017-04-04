<?php
namespace App\Helpers\Traits;

use Illuminate\Http\Request;

trait SafeRecord {
    protected $request_params;

    //This method takes a request and loops through it to get certain attributes and stores them in an array
    //If one attribute is not found in the request the key/value pair will be simply not be there (better than
    //setting it to null because we do not necessarily need it to be null)
    protected function grab_from_request(Request $request, array $attributes) {
        $this->request_params = [];
        foreach ($attributes as $attribute) {
                if ($request->exists($attribute)) {
                    $file = $request->hasFile($attribute);
                    $this->request_params[$attribute] = $file ? $request->file($attribute) : $request->get($attribute);
                }
            }
            return $this->request_params;
    }
    //This loops through the prepared request items and stores them safely (no need for mass assignment)
    public function safeRecord(Request $request, array $attributes, array $outside_request_attributes = []) {
        $request_params = $this->grab_from_request($request, $attributes);
        foreach ($request_params as $request_key => $request_value) {
            $this->setAttribute($request_key, $request_value);
        }
        foreach ($outside_request_attributes as $attribute_key => $attribute_value) {
            $this->setAttribute($attribute_key, $attribute_value);
        }
        $this->save();
        return $this;
    }
    public function safeSaver(array $fields) {
        foreach ($fields as $field_key => $field_value) {
            $this->setAttribute($field_key, $field_value);
        }
        $this->save();
        return $this;
    }
}