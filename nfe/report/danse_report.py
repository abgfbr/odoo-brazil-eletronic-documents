# -*- encoding: utf-8 -*-
# Copyright (C) 2017  KMEE
# Copyright (C) 2018  ABGF
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from datetime import datetime
from openerp import api
from openerp.addons.report_py3o.py3o_parser import py3o_report_extender


def format_money_mask(value):
    """
    Function to transform float values to pt_BR currency mask
    :param value: float value
    :return: value with brazilian money format
    """
    import locale
    locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
    value_formated = locale.currency(value, grouping=True)

    return value_formated[3:]

@api.model
@py3o_report_extender("nfe.danse_py3o_report")
def analytic_report(pool, cr, uid, local_context, context):
    """
    :return:
    """
    proxy = pool['account.invoice']
    invoice = proxy.browse(cr, uid, context['active_id'])

    data = {
        "num_nota": invoice.internal_number,
        "data_envio": datetime.strptime(invoice.date_hour_invoice, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S"),
        "data_competencia": datetime.strptime(invoice.date_in_out, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y"),
        "cod_nota": invoice.nfe_access_key if invoice.nfe_access_key else '',
        "tomador": 'Tomador' if invoice.issqn_value_wh > 0 else '',
        "cnpj_cpf_tomador": invoice.partner_id.cnpj_cpf,
        "razao_social_tomador": invoice.partner_id.legal_name,
        "endereco_tomador": invoice.partner_id.street,
        "complemento_tomador": invoice.partner_id.street2,
        "cep_tomador": invoice.partner_id.zip,
        "telefone_tomador": invoice.partner_id.phone,
        "im_tomador": invoice.partner_id.inscr_est,
        "numero_tomador": invoice.partner_id.number,
        "bairro_tomador": invoice.partner_id.district,
        "cidade_tomador": invoice.partner_id.l10n_br_city_id.name,
        "uf_tomador": invoice.partner_id.state_id.name,
        "cidade_uf_tomador": "{}/{}".format(invoice.partner_id.l10n_br_city_id.name, invoice.partner_id.state_id.name),
        "email_tomador": invoice.partner_id.email,
        "descricao_servico": invoice.invoice_line.fiscal_comment,
        "servico_code": invoice.invoice_line.product_id.service_type_id.code,
        "servico_code_formated": invoice.invoice_line.product_id.service_type_id.code.replace(".", ""),
        "servico_desc": invoice.invoice_line.product_id.service_type_id.name,
        "aliquota_iss": str(invoice.invoice_line.issqn_percent).replace(".",","),
        "cnae": invoice.company_id.cnae_main_id.code.replace("-", "").replace("/", ""),
        "total_bruto": format_money_mask(invoice.amount_total),
        "iss_retido": "Sim" if invoice.issqn_value_wh > 0 else "Não",
        "iss": format_money_mask(invoice.issqn_value) if invoice.issqn_value_wh <= 0 else "0,00",
        "pis": format_money_mask(invoice.pis_value_wh),
        "cofins": format_money_mask(invoice.cofins_value_wh),
        "inss": format_money_mask(invoice.inss_value_wh),
        "irrf": format_money_mask(invoice.irrf_value_wh),
        "csll": format_money_mask(invoice.csll_value_wh),
        "iss_retido_valor": format_money_mask(invoice.issqn_value_wh),
        "total_liquido": format_money_mask(invoice.amount_net),
        "informacoes_adicional": invoice.fiscal_comment,
    }

    local_context.update(data)
