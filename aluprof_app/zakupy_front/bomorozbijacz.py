from flask import render_template,  request, flash, url_for, redirect
from flask_wtf import FlaskForm
from aluprof_app import logger
from aluprof_app.zakupy_front import zakupy_front_bp
from aluprof_app.utils import oracle_query_to_dict
from wtforms import TextAreaField, RadioField
from wtforms.validators import DataRequired
from datetime import datetime


class BomFormList(FlaskForm):
    list_of_bom = TextAreaField('Lista bomów',
                                validators=[DataRequired("Podaj pozycję do rozbicia")],
                                render_kw={"rows": 70, "cols": 11})
    all_boms = RadioField('Poziom rozbicia',
                          choices=[(0, 'Wszystkie bomy'), (1, 'Ostatni poziom')],
                          default=1)


@zakupy_front_bp.route('/bom', methods=['POST', 'GET'])
def bomorozbijacz():

    try:
        form = BomFormList()
        if form.validate_on_submit() and request.method == 'POST':
            lista = form.list_of_bom.data.split()
            lista = "('         " + "', '         ".join(lista).upper() + "')"
            query = """select * from Book"""
            print(f'Bomorozbijacz -> IP: {request.remote_addr}, Czas: {datetime.now()}, Dane: {lista}, Bom: {form.all_boms.data}')
            headers, pakiet = oracle_query_to_dict(query)
            return render_template('bomorozbijacz.html', form=form, dane=pakiet, headers=headers)
        else:
            return render_template('bomorozbijacz.html', form=form)
    except Exception as err:
        logger.error(
            f'{request.host_url}: Proces bomorozbijacz przerwany, Bład: {err}')
        flash(message=f'Podczas wykonywania opracji pojawił sie błąd:\n'
                      f'{err}.\n'
                      f'Skontaktuj się z administraotrem.', category='danger')
        return redirect(url_for('zakupy_front.index'))
