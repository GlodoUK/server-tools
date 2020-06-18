from odoo import api, models


class Base(models.AbstractModel):
    _inherit = 'base'

    def play_onchanges_filtered(self, vals, onchange_keys):
        vals_to_readd = {}
        this_onchange_keys = onchange_keys

        safe_keys = list(self.fields_get().keys())

        unsafe_keys = []

        for key, _val in vals.items():
            if key not in safe_keys:
                unsafe_keys.append(key)

        for unsafe_key in unsafe_keys:
            vals_to_readd[unsafe_key] = vals.pop(unsafe_key)

            if unsafe_key in this_onchange_keys:
                this_onchange_keys.remove(unsafe_key)

        vals = self.play_onchanges(vals, this_onchange_keys)
        vals.update(vals_to_readd)

        return vals

    @api.model
    def play_onchanges_inherits(self, vals, onchange_keys):
        # play the onchange events for each thing we inherit from
        # we need to carefully remove and readd any values that are unknown for
        # each inherited model

        if hasattr(self, '_inherits'):
            for inherited_model in self._inherits.keys():
                vals = self.env[inherited_model].play_onchanges_filtered(vals, onchange_keys)

        return vals
