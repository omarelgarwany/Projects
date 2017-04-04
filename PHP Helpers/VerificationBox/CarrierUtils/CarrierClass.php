<?php
/**
 * Created by PhpStorm.
 * User: omar
 * Date: 03/12/15
 * Time: 06:55 م
 */

namespace App\VerificationBox\CarrierUtils;

use \App\SuperModel\SuperModel;
class CarrierClass implements CarrierInterface
{
    protected $verification_params;
    protected $buffer_record;

    public function setLabels($params) {
        $this->verification_params = $params;
    }
    public function getVerificationParams() {
        return $this->verification_params;
    }
    public function copyRow(SuperModel $oldModel) {
        $buffer_record = $oldModel->grabByParamsFirst($this->verification_params);
        $this->buffer_record = ($buffer_record);

    }

    public function grabRow(SuperModel $oldModel)
    {
            $buffer_record = $oldModel->grabByParamsFirst($this->verification_params);
            $oldModel->destroyByParams($this->verification_params);
            $this->buffer_record = ($buffer_record);
    }
    public function putRow(SuperModel $newModel)
    {
        $newModel->createByParams($this->buffer_record);
    }

    public function addRemoveStuff($additional, $removed) {
        foreach ($additional as $key => $val) {
            $this->buffer_record[$key] = $val;
        }
        foreach ($removed as $key => $val) {
            array_forget($this->buffer_record, $val);
        }

    }
    public function showTheRow() {
        return $this->buffer_record;
    }
}
