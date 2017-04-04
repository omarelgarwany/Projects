<?php
namespace App\Helpers\Traits;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

trait JsonValidationable {
    protected function validateRequest(Request $request, array $validation_rules) {
        $validator = Validator::make($request->all(), $validation_rules);
        if ($validator->fails()) {
            return ['success' => false, 'error_code' => 2, 'errors' => $validator->errors()];
        }
        return null;
    }
}