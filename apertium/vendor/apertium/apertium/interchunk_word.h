/*
 * Copyright (C) 2005 Universitat d'Alacant / Universidad de Alicante
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, see <https://www.gnu.org/licenses/>.
 */

#ifndef _INTERCHUNKWORD_
#define _INTERCHUNKWORD_

#include <apertium/apertium_re.h>
#include <map>
#include <string>
#include <lttoolbox/ustring.h>

using namespace std;

/**
 * Word type for transfer modules
 */
class InterchunkWord
{
private:
  /**
   * Target language chunk name and tags
   */
  UString chunk;

  /**
   * Target language chunk content
   */
  UString queue;
  
  /**
   * Wordbound blank (for postchunk)
   */
  UString wblank;

  /**
   * Copy method
   * @param o the object to be copied
   */
  void copy(InterchunkWord const &o);

  /**
   * Destroy method
   */
  void destroy();

public:
  /**
   * Non-parametric constructor
   */
  InterchunkWord();
  /**
   * Destructor
   */
  ~InterchunkWord();

  /**
   * Copy constructor
   * @param o the object to be copied
   */
  InterchunkWord(InterchunkWord const &o);

  /**
   * Parametric constructor calling init()
   * @param chunk the chunk
   */
  InterchunkWord(UString const &chunk);

  /**
   * Assignment operator
   * @param o the object to be assigned
   * @return reference to left part of assignment
   */
  InterchunkWord & operator =(InterchunkWord const &o);

  /**
   * Sets a chunk
   * @param chunk the chunk
   */
  void init(UString const &chunk);

  /**
   * Reference a chunk part
   * @param part regular expression to match
   * @returns reference to the part of string matched
   */
  UString chunkPart(ApertiumRE const &part);
  
  /**
   * Reference the wordbound blank (for postchunk)
   * @returns reference to the wblank string
   */
  UString getWblank();

  /**
   * Sets a value for a chunk part
   * @param part regular expression to match
   * @param value the new value for the given part
   * @returns whether part matched
   */
  bool setChunkPart(ApertiumRE const &part, UString const &value);

};

#endif
