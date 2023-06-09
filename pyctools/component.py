# ipdb is a debugger (pip install ipdb)
import pkg_resources
import pydantic
import typing
import pandas as pd
from .core import BaseModel
from .automaton import PycAutomaton, PycState
installed_pkg = {pkg.key for pkg in pkg_resources.working_set}
if 'ipdb' in installed_pkg:
    import ipdb  # noqa: F401


class PycVariable(BaseModel):
    id: str = pydantic.Field(..., description="Variable id")
    name: str = pydantic.Field(None, description="Variable name")
    comp_name: str = pydantic.Field(None, description="Component name")
    value_init: typing.Any = pydantic.Field(None, description="Variable init value")
    value_current: typing.Any = pydantic.Field(None, description="Current value")
    bkd: typing.Any = pydantic.Field(None, description="Variable backend handler")

    @classmethod
    def from_bkd(basecls, bkd):

        return basecls(
            id=bkd.name(),
            name=bkd.basename(),
            comp_name=bkd.parent().name(),
            value_init=bkd.initValue(),
            value_current=bkd.value(),
            bkd=bkd)

    
class PycComponent(BaseModel):

    name: str = pydantic.Field(..., description="Component name")
    variables: typing.List[PycVariable] = pydantic.Field([], description="Variable list")
    states: typing.List[PycState] = pydantic.Field([], description="state list")
    automata: typing.List[PycAutomaton] = pydantic.Field([], description="Automata list")
    bkd: typing.Any = pydantic.Field(None, description="Component backend handler")

    @pydantic.validator('states', pre=True)
    def check_states(cls, value, values, **kwargs):
        value = [PycState(**v) for v in value]
        return value

    @pydantic.validator('variables', pre=True)
    def check_variables(cls, value, values, **kwargs):
        value = [PycVariable.from_dict(**v) for v in value]
        return value

    # @pydantic.validator('automata', pre=True)
    # def check_automata(cls, value, values, **kwargs):
    #     value = [PycAutomaton(**v) for v in value]
    #     return value

    def get_automaton_by_name(self, name):

        for elt in self.automata:
            if elt.name == name:
                return elt

        raise ValueError(f"Automaton {name} is not part of component {self.name}")

    def get_variable_by_name(self, name):

        for elt in self.variables:
            if elt.name == name:
                return elt

        raise ValueError(f"Variable {name} is not part of component {self.name}")

    
    @classmethod
    def from_bkd(basecls, bkd):

        comp = basecls(name=bkd.name(), bkd=bkd)
        comp.variables = \
            [PycVariable.from_bkd(elt) for elt in bkd.getVariables()]
        comp.states = \
            [PycState.from_bkd(elt) for elt in bkd.getStates()]
        comp.automata = \
            [PycAutomaton.from_bkd(elt) for elt in bkd.getAutomata()]

        return comp

    def to_df(self):

        df_var = pd.DataFrame(
            [var.dict(exclude={"bkd", "id"})
             for var in self.variables])

        df_var["type"] = "VAR"

        aut_dict_list = []
        for aut in self.automata:
            aut_dict = \
                aut.dict(exclude={"bkd", "id",
                                  "states", "transitions",
                                  "init_state"})

            aut_dict.update(
                value_init=aut.init_state,
                value_current=aut.get_active_state().name,
            )

            aut_dict_list.append(aut_dict)
            
        df_aut = pd.DataFrame(aut_dict_list)
        df_aut["type"] = "ST"
            
        df = pd.concat([df_var, df_aut],
                       axis=0, ignore_index=True)

        return df
