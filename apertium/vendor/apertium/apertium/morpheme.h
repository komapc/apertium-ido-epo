// Copyright (C) 2005 Universitat d'Alacant / Universidad de Alicante
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License as
// published by the Free Software Foundation; either version 2 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, see <https://www.gnu.org/licenses/>.

#ifndef MORPHEME_H
#define MORPHEME_H

#include <lttoolbox/ustring.h>
#include <lttoolbox/input_file.h>
#include <vector>
#include <iostream>

namespace Apertium {
class Morpheme {
public:
  friend bool operator==(const Morpheme &a, const Morpheme &b);
  friend bool operator<(const Morpheme &a, const Morpheme &b);
  friend std::ostream& operator<<(std::ostream& out, const Morpheme &morph);
  operator UString() const;
  void read(InputFile& in);
  UString TheLemma;
  std::vector<UString> TheTags;
};
}

#endif // MORPHEME_H
