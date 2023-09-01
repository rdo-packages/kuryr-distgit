%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815AFEC729392386480E076DCC0DFE2D21C023C9
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
%global with_doc 1

%global project kuryr
%global library kuryr-lib
%global egg kuryr_lib

%global common_desc OpenStack Kuryr library shared by all Kuryr sub-projects.

Name: python-%library
Version: 2.8.0
Release: 1%{?dist}
Summary: OpenStack Kuryr library
License:    Apache-2.0
URL:        http://docs.openstack.org/developer/kuryr

Source0:    https://tarballs.openstack.org/%{project}/%{library}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{project}/%{library}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch: noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%package -n python3-%{library}
Summary: OpenStack Kuryr library


BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description -n python3-%{library}
%{common_desc}

%package -n python3-%{library}-tests
Summary:    OpenStack Kuryr library tests
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-ddt
Requires:   python3-oslotest
Requires:   python3-testtools

%description -n python3-%{library}-tests
%{common_desc}

This package contains the Kuryr library test files.

%if 0%{?with_doc}
%package doc
Summary:    OpenStack Kuryr library documentation

%description doc
%{common_desc}

This package contains the documentation.
%endif

%package -n kuryr-binding-scripts
Summary:    OpenStack Kuryr binding scripts for SDNs

Requires: bash
Requires: iproute

%description -n kuryr-binding-scripts
%{common_desc}

This package contains the binding scripts for different SDNs.

%description
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{library}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
%tox -e %{default_toxenv}

%files -n python3-%{library}
%license LICENSE
%{_bindir}/%{project}-status
%{python3_sitelib}/%{project}
%{python3_sitelib}/%{egg}-*.dist-info
%exclude %{python3_sitelib}/%{project}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{project}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%files -n kuryr-binding-scripts
%license LICENSE
%{_libexecdir}/kuryr

%changelog
* Fri Sep 01 2023 RDO <dev@lists.rdoproject.org> 2.8.0-1
- Update to 2.8.0

