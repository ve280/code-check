#ifndef INSTR_H
#define INSTR_H

#include <iostream>
#include <string>

enum class InstrName {ADD, NOR, IFZ, HALT, LOAD, STORE, POP, PUSHI, NOOP};

const std::string instrPrint[] = {"ADD", "NOR", "IFZ", "HALT", "LOAD", "STORE", "POP", "PUSHI", "NOOP"};

struct Instr {
    InstrName name;
    int parameter;
    friend std::ostream& operator<< (std::ostream& os, const Instr& it) {
        os << instrPrint[static_cast<int>(it.name)];
        if (it.name == InstrName::PUSHI || it.name == InstrName::IFZ) {
            os << " " << it.parameter;
        }
        return os;
    }
};

std::istream& operator>>(std::istream& is, Instr& it)
{
    std::string s;
    is >> s;
    auto ptr = std::find(instrPrint, instrPrint + 9, s);
    it.name = static_cast<InstrName>(ptr - instrPrint);
    if (it.name == InstrName::PUSHI || it.name == InstrName::IFZ) {
        is >> it.parameter;
    }
    return is;
}

#endif