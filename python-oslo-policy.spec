%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
%global pypi_name oslo.policy
%global pkg_name oslo-policy
%global with_doc 1
%global common_desc \
An OpenStack library for policy.

%global common_desc1 \
Test subpackage for the Oslo policy library.

Name:           python-%{pkg_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack oslo.policy library

License:        Apache-2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{pkg_name}
Summary:        OpenStack oslo.policy library
Obsoletes: python2-%{pkg_name} < %{version}-%{release}

BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo policy library

%description -n python-%{pkg_name}-doc
Documentation for the Oslo policy library.
%endif

%package -n python3-%{pkg_name}-tests
Summary:    Test subpackage for the Oslo policy library

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-hacking
Requires:  python3-oslotest
Requires:  python3-fixtures
Requires:  python3-mock
Requires:  python3-requests

%description -n python3-%{pkg_name}-tests
%{common_desc1}

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo policy library

%description -n python-%{pkg_name}-lang
Translation files for Oslo policy library

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# FIXME (jpena): Remove buggy PO-Revision-Date lines in translation
# See https://bugs.launchpad.net/openstack-i18n/+bug/1586041 for details
sed -i '/^\"PO-Revision-Date: \\n\"/d' oslo_policy/locale/*/LC_MESSAGES/*.po

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
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%install
%pyproject_install

# Generate i18n files
python3 setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/oslo_policy/locale --domain oslo_policy

pushd %{buildroot}/%{_bindir}
for item in checker list-redundant policy-generator sample-generator
do
  # Create a versioned binary for backwards compatibility until everything is pure py3
  ln -s oslopolicy-$item %{buildroot}%{_bindir}/oslopolicy-$item-3
done
popd

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_policy/locale/*/LC_*/oslo_policy*po
rm -f %{buildroot}%{python3_sitelib}/oslo_policy/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_policy/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_policy --all-name

%check
export OS_TEST_PATH="./oslo_policy/tests"
%tox -e %{default_toxenv}

%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{_bindir}/oslopolicy-policy-upgrade
%{_bindir}/oslopolicy-checker
%{_bindir}/oslopolicy-checker-3
%{_bindir}/oslopolicy-convert-json-to-yaml
%{_bindir}/oslopolicy-list-redundant
%{_bindir}/oslopolicy-list-redundant-3
%{_bindir}/oslopolicy-policy-generator
%{_bindir}/oslopolicy-policy-generator-3
%{_bindir}/oslopolicy-sample-generator
%{_bindir}/oslopolicy-sample-generator-3
%{_bindir}/oslopolicy-validator
%{python3_sitelib}/oslo_policy
%{python3_sitelib}/*.dist-info
%exclude %{python3_sitelib}/oslo_policy/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_policy/tests

%files -n python-%{pkg_name}-lang -f oslo_policy.lang
%license LICENSE

%changelog

